import logging
import sqlalchemy
import shortuuid
import json
import os
import time
import asyncio
import threading
import shutil

from datetime import datetime, timedelta, timezone
from rx.subject import Subject

from db import get_db, metadata
from config import LOCAL_STORAGE_PATH, REMOTE_STORAGE_PATH

from controllers.controller import Controller
from controllers.participants import participant_controller
from controllers.cameras import camera_controller
from controllers.studies import studies_controller

from gpiozero import LED

#trigger for TMSi Porti, pin1 = 3.3V (GND = pin6)
trigger = LED("GPIO21") #LED("BOARD40")
led_red = LED("GPIO5") #LED("BOARD29")
led_yellow = LED("GPIO6") #LED("BOARD31")
led_green = LED("GPIO13") #LED("BOARD33")
led_blue = LED("GPIO19") #LED("BOARD35")
led_white = LED("GPIO26") #LED("BOARD")

logging.basicConfig(level=logging.DEBUG,
                    format='%(relativeCreated)6d %(threadName)s %(message)s')

logger = logging.getLogger()
database = get_db()

recordings = sqlalchemy.Table('recordings', metadata,
                              sqlalchemy.Column(
                                  'id', sqlalchemy.String, primary_key=True),
                              sqlalchemy.Column(
                                  'participant_id', sqlalchemy.ForeignKey('participants.id')),
                              sqlalchemy.Column('name', sqlalchemy.String),
                              sqlalchemy.Column(
                                  'file_path', sqlalchemy.String),
                              sqlalchemy.Column(
                                  'start_time', sqlalchemy.String),
                              sqlalchemy.Column('end_time', sqlalchemy.String),
                              sqlalchemy.Column('state', sqlalchemy.String),

                              sqlalchemy.Column(
                                  'cameras_recorded', sqlalchemy.String),
                              sqlalchemy.Column(
                                  'cameras_processing', sqlalchemy.String),
                              sqlalchemy.Column(
                                  'cameras_processed', sqlalchemy.String),
                              )


class RecordingController(Controller):
    sessions = {}
    observable = Subject()

    def parse_row(self, row):
        return {
            'id': row['id'],
            'participant_id': row['participant_id'],
            'name': row['name'],
            'file_path': row['file_path'],
            'start_time': row['start_time'],
            'end_time': row['end_time'],
            'state': row['state'],
            'cameras_recorded': json.loads(row['cameras_recorded']),
            'cameras_processing': json.loads(row['cameras_processing']),
            'cameras_processed': json.loads(row['cameras_processed']),
        }

    async def get_recording_metadata(self, recording):
        participant = await participant_controller.get(recording.get('participant_id'))
        study = await studies_controller.get(participant.get('study_id'))

        return {
            'recording_name': recording.get('name'),
            'start_time': recording.get('start_time'),
            'end_time': recording.get('end_time'),
            'participant_number': participant.get('number'),
            'study_name': study.get('name'),
            'researcher': study.get('researcher'),
        }

    async def get_recording_path(self, recording):
        participant = await participant_controller.get(recording.get('participant_id'))
        study = await studies_controller.get(participant.get('study_id'))
        path = '{}_{}_{}'.format(study.get('name'),
                                 participant.get('number'),
                                 recording.get('name'))

        return path.replace(' ', '_').replace(':', '_').replace('-', '_')

    async def get_local_storage_path(self, recording):
        recording_path = await self.get_recording_path(recording)
        return '{}/{}'.format(LOCAL_STORAGE_PATH, recording_path)

    async def get_remote_storage_path(self, recording):
        recording_path = await self.get_recording_path(recording)
        return '{}/{}'.format(REMOTE_STORAGE_PATH, recording_path)

    async def get_camera_file_path(self, recording, camera_id):
        local_path = await self.get_local_storage_path(recording)

        camera = await camera_controller.get(camera_id)
        return '{}_{}.mp4'.format(local_path, camera.get('name', camera_id).replace(' ', '_'))

#new start
    async def sendtrigger(self, recording):
        start_time = recording.get('start_time')
        current_time = datetime.now().astimezone()

        while current_time < start_time and self.recording:
            time.sleep(0.001)
            current_time = datetime.now().astimezone()
        trigger.on()
        time.sleep(2)
        trigger.off()
#new end

    async def start(self, recording_id):
        async with self.db.transaction():
            recording = await self.get(recording_id)
            if not recording:
                return

            recording['start_time'] = (
                datetime.now() + timedelta(seconds=3)).astimezone().isoformat()
            recording['end_time'] = None
            recording['state'] = 'recording'
            recording['cameras_processed'] = []
            recording['cameras_processing'] = []

            cameras_recorded = await camera_controller.send_command({
                'event': 'start_recording',
                'data': recording,
            })

            recording['cameras_recorded'] = cameras_recorded
            recording = await self.update(recording)

            #send trigger to TMSi Porti
            thread = threading.Thread(
                target=self.sendtrigger, args=(recording), daemon=True)
            thread.start()
            
            return recording

    async def stop(self, recording_id):
        async with self.db.transaction():
            recording = await self.get(recording_id)
            if not recording:
                return

            await camera_controller.send_command({
                'event': 'stop_recording',
                'data': recording,
            })

            recording['end_time'] = datetime.now().astimezone().isoformat()
            recording['state'] = 'unprocessed'
            recording = await self.update(recording)

            return recording

    async def discard(self, recording_id):
        async with self.db.transaction():
            recording = await self.get(recording_id)
            if not recording:
                return

            await camera_controller.send_command({
                'event': 'discard_recording',
                'data': recording,
            })

            recording['start_time'] = None
            recording['end_time'] = None
            recording['cameras_recorded'] = []
            recording['state'] = 'empty'
            recording = await self.update(recording)

            return recording

    async def process(self, recording_id):
        async with self.db.transaction():
            await self.db.execute('LOCK TABLE recordings IN SHARE ROW EXCLUSIVE MODE')

            recording = await self.get(recording_id)
            if not recording:
                return

            local_storage_path = await self.get_local_storage_path(recording)
            remote_storage_path = await self.get_remote_storage_path(recording)

            if not os.path.exists(remote_storage_path):
                os.makedirs(remote_storage_path)

            recording_metadata = await self.get_recording_metadata(recording)
            metadata_path = '{}/metadata.json'.format(remote_storage_path)

            with open(metadata_path, 'w') as file:
                file.write(json.dumps(recording_metadata, indent=2))

            cameras_processing = await camera_controller.send_command({
                'event': 'process_recording',
                'data': recording,
            })

            recording['cameras_processing'] = cameras_processing
            recording['cameras_processed'] = []
            recording['state'] = 'processing'
            recording = await self.update(recording)

            return recording

    async def processed(self, recording_id, camera_id):
        recording = await self.get(recording_id)
        camera = await camera_controller.get(camera_id)

        source = await self.get_camera_file_path(recording, camera_id)
        base_path = await self.get_remote_storage_path(recording)
        dest = '{}/{}.mp4'.format(base_path, camera.get('name', camera_id))

        thread = threading.Thread(
            target=self.upload, args=(source, dest), daemon=True)
        thread.start()

        async with self.db.transaction():
            await self.db.execute('LOCK TABLE recordings IN SHARE ROW EXCLUSIVE MODE')

            recording = await self.get(recording.get('id'))
            if not recording:
                return

            recording['cameras_processing'].remove(camera_id)
            recording['cameras_processed'].append(camera_id)
            if len(recording['cameras_processing']) == 0:
                recording['state'] = 'processed'

            recording = await self.update(recording)

        return recording

    def upload(self, source, dest):
        logger.info('Upload {} to {}'.format(source, dest))
        shutil.move(source, dest)
        logger.info('Done uploading {}'.format(dest))

    async def get_all(self):
        query = recordings.select()
        results = await self.db.fetch_all(query)
        return [self.parse_row(result) for result in results]

    async def create(self, recording):
        recording_id = shortuuid.uuid()
        query = recordings.insert().values(
            id=recording_id,
            participant_id=recording.get('participant_id'),
            name=recording.get('name'),
            file_path=recording.get('file_path'),
            start_time=recording.get('start_time'),
            end_time=recording.get('end_time'),
            cameras_recorded=json.dumps([]),
            cameras_processing=json.dumps([]),
            cameras_processed=json.dumps([]),
            state='empty',
        )
        await self.db.execute(query)

        recording = await self.get(recording_id)
        await self.broadcast({
            'event': 'create',
            'entity': recording
        })
        return recording

    async def get(self, recording_id):
        query = recordings.select().where(recordings.c.id == recording_id)
        result = await self.db.fetch_one(query)
        if result:
            return self.parse_row(result)

    async def update(self, recording):
        query = recordings.update().where(recordings.c.id == recording.get('id')).values(
            id=recording.get('id'),
            participant_id=recording.get('participant_id'),
            name=recording.get('name'),
            file_path=recording.get('file_path'),
            start_time=recording.get('start_time'),
            end_time=recording.get('end_time'),
            cameras_recorded=json.dumps(recording.get('cameras_recorded')),
            cameras_processing=json.dumps(recording.get('cameras_processing')),
            cameras_processed=json.dumps(recording.get('cameras_processed')),
            state=recording.get('state'),
        )
        await self.db.execute(query)

        recording = await self.get(recording.get('id'))
        await self.broadcast({
            'event': 'update',
            'entity': recording
        })
        return recording

    async def delete(self, recording_id):
        recording = await self.get(recording_id)

        query = recordings.delete().where(recordings.c.id == recording_id)
        await self.db.execute(query)

        await self.broadcast({
            'event': 'delete',
            'entity': recording
        })
        return recording


recording_controller = RecordingController()

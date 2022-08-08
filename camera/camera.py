import io
import asyncio
import os
import logging
import time
import requests
import json
import subprocess
import shutil

from picamera import PiCamera
from datetime import datetime
from preview import output

logger = logging.getLogger()


class CameraController():
    camera = PiCamera(
        framerate=30,
        resolution=(800, 600),
    )

    recording = False
    diagnostic = False
    recording_local_base_path = '/home/pi/local'

    def get_recording_local_path(self, recording_id):
        return '{}/{}.h264'.format(self.recording_local_base_path, recording_id)

    def get_recording_output_path(self, storage_path):
        return '{}/{}.mp4'.format(storage_path, os.environ['CAMERA_ID'])

    def on_start_recording(self, recording):
        self.stop_preview()

        logger.info('Start recording {}'.format(recording.get('id')))

        try:
            if self.recording:
                logger.error(
                    'Already recording. Ignoring recording {}...'.format(recording))

            self.diagnostic = None
            if recording.get('is_diagnostic'):
                self.diagnostic = {
                    'diagnostic_id': recording.get('diagnostic_id'),
                    'iteration': recording.get('iteration'),
                    'camera_id': os.environ['CAMERA_ID'],
                    'time_start_requested': recording.get('start_time'),
                    'time_socket_received': datetime.now().astimezone().isoformat(),
                }
                logger.info('Performing diagnostic recording...')

            if self.diagnostic:
                self.diagnostic['time_recording_start'] = datetime.now(
                ).astimezone().isoformat()

            # This will loop til the start time of the recording
            start_time = datetime.fromisoformat(recording.get('start_time'))
            logger.info('Waiting until {} to start capturing video...'.format(
                recording.get('start_time')))

            recording_path = self.get_recording_local_path(recording.get('id'))
            try:
                os.makedirs(self.recording_local_base_path)
                os.remove(recording_path)
            except:
                pass

            logger.info('Recording id: {}, with recording path: {}'.format(
                recording.get('id'), recording_path))

            self.recording = True

            current_time = datetime.now().astimezone()
            while current_time < start_time and self.recording:
                time.sleep(0.001)
                current_time = datetime.now().astimezone()

            if self.recording:
                self.camera.start_recording(recording_path,
                                            # '/dev/null',
                                            format='h264',
                                            # the highest available h264 encoding level
                                            level='4.2',
                                            # 10 is the highest, 40 the lowest
                                            quality=20,
                                            # include fps headers in the video
                                            sps_timing=True,
                                            # we set this to 1 so that the split_recording splits on the next frame
                                            # intra_period=1,
                                            # this (hopefully) reduces the motion blur
                                            # intra_refresh='both',
                                            # embed enhancement information in the frames
                                            sei=True,
                                            # exposure_mode='sports',
                                            # motion_output = motion_output,
                                            )

                if self.diagnostic:
                    self.diagnostic['time_recording_started'] = datetime.now(
                    ).astimezone().isoformat()

                logger.info(
                    'Started capturing video at {}... '.format(datetime.now()))

                while self.recording:
                    self.camera.wait_recording(0.02)

        finally:
            if self.diagnostic:
                self.diagnostic['time_recording_stop'] = datetime.now(
                ).astimezone().isoformat()

            self.camera.stop_recording()

            logger.info(
                'Stopped capturing video at {}... '.format(datetime.now()))

            if self.diagnostic:
                self.diagnostic['time_recording_stopped'] = datetime.now(
                ).astimezone().isoformat()

                logger.info('Sending diagnostic {}'.format(self.diagnostic))
                requests.post(url='http://{}/api/diagnostic_results/'.format(os.environ['CONTROLLER_HOST']),
                              data=json.dumps(self.diagnostic))

            self.start_preview()

    def on_stop_recording(self, recording):
        self.recording = False

    def on_discard_recording(self, recording):
        recording_path = self.get_recording_local_path(recording.get('id'))
        logger.info('Discard the recording {}'.format(recording_path))

        try:
            os.remove(recording_path)
        except:
            pass

    def on_process_recording(self, data):
        recording = data.get('recording')
        recording_path = self.get_recording_local_path(recording.get('id'))
        output_path = self.get_recording_output_path(data.get('storage_path'))

        logger.info('Process the recording from {} to {}'.format(
            recording_path, output_path))

        try:
            os.remove(output_path)
        except:
            pass

        try:
            # TODD:change! hard-coded fps
            subprocess.run(
                ['MP4Box', '-fps', '30', '-add', recording_path, output_path],
                check=True,
                text=True,
            )
            # logger.info('MP4Box output:\n{}'.format(result.stdout))
        except Exception as e:
            logger.error(
                'Error converting h264 to mp4\nerror: {}'.format(e))
            return

        logger.info('Processed the recording succesfully'.format(
            recording_path, output_path))

        requests.get(url='http://{}/api/recordings/{}/processed/{}'.format(
            os.environ['CONTROLLER_HOST'],
            recording.get('id'),
            os.environ['CAMERA_ID']
        ))

        try:
            shutil.rmtree(self.recording_local_base_path)
        except:
            pass

    async def force_stop(self):
        self.recording = False

    def start_preview(self):
        try:
            self.camera.start_recording(output, format='mjpeg')
            logger.info("Started preview...")

        except subprocess.CalledProcessError as e:
            logger.error(
                'Error starting preview {} {}'.format(e.cmd, e.output))
            return

    def stop_preview(self):
        try:
            self.camera.stop_recording()
            logger.info("Stopped preview...")
        except subprocess.CalledProcessError as e:
            logger.error(
                'Error stopping preview {} {}'.format(e.cmd, e.output))
            return

import logging
import sqlalchemy
import shortuuid
import asyncio
import time

from datetime import datetime, timedelta
from rx.subject import Subject

from db import metadata
from controllers import camera_controller
from controllers.controller import Controller


logger = logging.getLogger()

diagnostics = sqlalchemy.Table('diagnostics', metadata,
                               sqlalchemy.Column(
                                   'id', sqlalchemy.String, primary_key=True),
                               sqlalchemy.Column(
                                   'start_time', sqlalchemy.String),
                               sqlalchemy.Column(
                                   'end_time', sqlalchemy.String),
                               sqlalchemy.Column(
                                   'iterations', sqlalchemy.Integer),
                               sqlalchemy.Column(
                                   'is_running', sqlalchemy.Boolean),
                               sqlalchemy.Column(
                                   'current_iteration', sqlalchemy.Integer),
                               )


class DiagnosticsController(Controller):
    def parse_row(self, row):
        return {
            'id': row['id'],
            'start_time': row['start_time'],
            'end_time': row['end_time'],
            'iterations': row['iterations'],
            'is_running': row['is_running'],
            'current_iteration': row['current_iteration'],
        }

    async def get_all(self):
        query = diagnostics.select()
        results = await self.db.fetch_all(query)
        return [self.parse_row(result) for result in results]

    async def run(self, diagnostic):
        for i in range(diagnostic['iterations']):
            iteration = i+1

            logger.info('Start diagnostic {} iteration {}'.format(
                diagnostic['id'], iteration))

            diagnostic['current_iteration'] = iteration
            await self.update(diagnostic)

            recording = {
                'id': 'diagnostic',
                'name': 'diagnostic',
                'file_path': 'diagnostic.h264',
                'start_time': (datetime.now() + timedelta(seconds=1)).astimezone().isoformat(),
                'end_time': None,
                'is_diagnostic': True,
                'diagnostic_id': diagnostic.get('id'),
                'iteration': iteration,
            }

            await camera_controller.send_command({
                'event': 'start_recording',
                'data': recording,
            })

            await asyncio.sleep(3)

            await camera_controller.send_command({
                'event': 'stop_recording',
                'data': recording,
            })

            logger.info('End diagnostic {} iteration {}'.format(
                diagnostic['id'], iteration))

            await asyncio.sleep(1)

        diagnostic['is_running'] = False
        diagnostic['end_time'] = datetime.now().astimezone().isoformat()

        await self.update(diagnostic)

    async def create(self, diagnostic):
        diagnostic_id = shortuuid.uuid()
        query = diagnostics.insert().values(
            id=diagnostic_id,
            start_time=diagnostic.get('start_time'),
            iterations=diagnostic.get('iterations'),
            current_iteration=diagnostic.get('current_iteration'),
            is_running=diagnostic.get('is_running'),
        )
        await self.db.execute(query)

        entity = await self.get(diagnostic_id)
        await self.broadcast({
            'event': 'create',
            'entity': entity
        })
        return entity

    async def get(self, diagnostic_id):
        query = diagnostics.select().where(diagnostics.c.id == diagnostic_id)
        result = await self.db.fetch_one(query)
        if result:
            return self.parse_row(result)

    async def update(self, result):
        query = diagnostics.update().where(diagnostics.c.id == result.get('id')).values(
            id=result.get('id'),
            start_time=result.get('start_time'),
            end_time=result.get('end_time'),
            iterations=result.get('iterations'),
            is_running=result.get('is_running'),
            current_iteration=result.get('current_iteration'),
        )
        await self.db.execute(query)

        entity = await self.get(result.get('id'))
        await self.broadcast({
            'event': 'update',
            'entity': entity
        })
        return entity

    async def delete(self, result_id):
        entity = await self.get(result_id)

        query = diagnostics.delete().where(diagnostics.c.id == result_id)
        await self.db.execute(query)

        await self.broadcast({
            'event': 'delete',
            'entity': entity
        })
        return entity


diagnostics_controller = DiagnosticsController()

import logging
import sqlalchemy
import shortuuid

from datetime import datetime
from rx.subject import Subject

from db import metadata
from controllers.controller import Controller


logger = logging.getLogger()

diagnostic_results = sqlalchemy.Table('diagnostics_results', metadata,
                                      sqlalchemy.Column(
                                          'id', sqlalchemy.String, primary_key=True),
                                      sqlalchemy.Column(
                                          'diagnostic_id', sqlalchemy.ForeignKey('diagnostics.id')),
                                      sqlalchemy.Column(
                                          'camera_id', sqlalchemy.ForeignKey('cameras.id')),
                                      sqlalchemy.Column(
                                          'iteration', sqlalchemy.Integer),
                                      sqlalchemy.Column(
                                          'time_start_requested', sqlalchemy.String),
                                      sqlalchemy.Column(
                                          'time_socket_received', sqlalchemy.String),
                                      sqlalchemy.Column(
                                          'time_preview_started', sqlalchemy.String),
                                      sqlalchemy.Column(
                                          'time_recording_start', sqlalchemy.String),
                                      sqlalchemy.Column(
                                          'time_recording_started', sqlalchemy.String),
                                      sqlalchemy.Column(
                                          'time_recording_stop', sqlalchemy.String),
                                      sqlalchemy.Column(
                                          'time_recording_stopped', sqlalchemy.String),
                                      )


class DiagnosticResultsController(Controller):
    def get_delta(self, col1, col2):
        delta = datetime.fromisoformat(col2) - datetime.fromisoformat(col1)
        return ((delta.seconds * 1000000) + delta.microseconds) / 1000

    def parse_row(self, row):
        return {
            'id': row['id'],
            'diagnostic_id': row['diagnostic_id'],
            'camera_id': row['camera_id'],
            'iteration': row['iteration'],
            'time_start_requested': row['time_start_requested'],
            'time_socket_received': row['time_socket_received'],
            'time_preview_started': row['time_preview_started'],
            'time_recording_start': row['time_recording_start'],
            'time_recording_started': row['time_recording_started'],
            'time_recording_stop': row['time_recording_stop'],
            'time_recording_stopped': row['time_recording_stopped'],
            'delta_sync': self.get_delta(row['time_start_requested'], row['time_recording_start']),
            'delta_recording': self.get_delta(row['time_start_requested'], row['time_recording_started']),
            'delta_start_preview': self.get_delta(row['time_socket_received'], row['time_preview_started']),
            'delta_start_recording': self.get_delta(row['time_recording_start'], row['time_recording_started']),
            'delta_stop_recording': self.get_delta(row['time_recording_stop'], row['time_recording_stopped']),
        }

    async def get_all(self, diagnostic_id=None):
        query = diagnostic_results.select()

        if diagnostic_id is not None:
            query = query.where(
                diagnostic_results.c.diagnostic_id == diagnostic_id)

        results = await self.db.fetch_all(query)
        return [self.parse_row(result) for result in results]

    async def create(self, result):
        result_id = shortuuid.uuid()
        query = diagnostic_results.insert().values(
            id=result_id,
            diagnostic_id=result.get('diagnostic_id'),
            camera_id=result.get('camera_id'),
            iteration=result.get('iteration'),
            time_start_requested=result.get('time_start_requested'),
            time_socket_received=result.get('time_socket_received'),
            time_preview_started=result.get('time_preview_started'),
            time_recording_start=result.get('time_recording_start'),
            time_recording_started=result.get('time_recording_started'),
            time_recording_stop=result.get('time_recording_stop'),
            time_recording_stopped=result.get('time_recording_stopped'),
        )
        await self.db.execute(query)

        entity = await self.get(result_id)
        await self.broadcast({
            'event': 'create',
            'entity': entity
        })
        return entity

    async def get(self, diagnostic_result_id):
        query = diagnostic_results.select().where(
            diagnostic_results.c.id == diagnostic_result_id)
        result = await self.db.fetch_one(query)
        if result:
            return self.parse_row(result)

    async def delete(self, result_id):
        entity = await self.get(result_id)

        query = diagnostic_results.delete().where(diagnostic_results.c.id == result_id)
        await self.db.execute(query)

        await self.broadcast({
            'event': 'delete',
            'entity': entity
        })
        return entity


diagnostic_results_controller = DiagnosticResultsController()

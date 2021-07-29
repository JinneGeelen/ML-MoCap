import logging
import sqlalchemy
import shortuuid
import asyncio
import time

from datetime import datetime, timedelta
from rx.subject import Subject

from db import get_db, metadata
from controllers.controller import Controller


logger = logging.getLogger()

studies = sqlalchemy.Table('studies', metadata,
                           sqlalchemy.Column(
                               'id', sqlalchemy.String, primary_key=True),
                           sqlalchemy.Column('name', sqlalchemy.String),
                           sqlalchemy.Column('researcher', sqlalchemy.String),
                           sqlalchemy.Column('date', sqlalchemy.String),
                           sqlalchemy.Column('emg', sqlalchemy.Boolean),
                           )


class StudiesController(Controller):
    @property
    def db(self):
        return get_db()

    def parse_row(self, row):
        return {
            'id': row['id'],
            'name': row['name'],
            'researcher': row['researcher'],
            'date': row['date'],
            'emg': row['emg'],
        }

    async def get_all(self):
        query = studies.select()
        results = await self.db.fetch_all(query)
        return [self.parse_row(result) for result in results]

    async def create(self, study):
        study_id = shortuuid.uuid()
        query = studies.insert().values(
            id=study_id,
            name=study.get('name'),
            researcher=study.get('researcher'),
            date=study.get('date'),
            emg=study.get('emg'),
        )
        await self.db.execute(query)

        study = await self.get(study_id)
        await self.broadcast({
            'event': 'create',
            'entity': study
        })
        return study

    async def get(self, study_id):
        query = studies.select().where(studies.c.id == study_id)
        study = await self.db.fetch_one(query)
        if study:
            return self.parse_row(study)

    async def update(self, study):
        query = studies.update().where(studies.c.id == study.get('id')).values(
            id=study.get('id'),
            name=study.get('name'),
            researcher=study.get('researcher'),
            date=study.get('date'),
            emg=study.get('emg'),
        )
        await self.db.execute(query)

        study = await self.get(study.get('id'))
        await self.broadcast({
            'event': 'update',
            'entity': study
        })
        return study

    async def delete(self, study_id):
        study = await self.get(study_id)

        query = studies.delete().where(studies.c.id == study_id)
        await self.db.execute(query)

        await self.broadcast({
            'event': 'delete',
            'entity': study
        })
        return study


studies_controller = StudiesController()

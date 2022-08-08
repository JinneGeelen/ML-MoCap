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

participants = sqlalchemy.Table('participants', metadata,
                                sqlalchemy.Column(
                                    'id', sqlalchemy.String, primary_key=True),
                                sqlalchemy.Column(
                                    'study_id', sqlalchemy.ForeignKey('studies.id')),
                                sqlalchemy.Column('number', sqlalchemy.String),
                                sqlalchemy.Column(
                                    'dominant_hand', sqlalchemy.String),
                                sqlalchemy.Column('age', sqlalchemy.Integer),
                                sqlalchemy.Column('gender', sqlalchemy.String),
                                sqlalchemy.Column(
                                    'consent_video', sqlalchemy.Boolean),
                                )


class ParticipantsController(Controller):
    def parse_row(self, row):
        return {
            'id': row['id'],
            'study_id': row['study_id'],
            'number': row['number'],
            'dominant_hand': row['dominant_hand'],
            'age': row['age'],
            'gender': row['gender'],
            'consent_video': row['consent_video'],
        }

    async def get_all(self):
        query = participants.select()
        results = await self.db.fetch_all(query)
        return [self.parse_row(result) for result in results]

    async def create(self, participant):
        participant_id = shortuuid.uuid()
        query = participants.insert().values(
            id=participant_id,
            study_id=participant.get('study_id'),
            number=participant.get('number'),
            dominant_hand=participant.get('dominant_hand'),
            age=participant.get('age'),
            gender=participant.get('gender'),
            consent_video=participant.get('consent_video'),
        )
        await self.db.execute(query)

        participant = await self.get(participant_id)
        await self.broadcast({
            'event': 'create',
            'entity': participant
        })
        return participant

    async def get(self, participant_id):
        query = participants.select().where(participants.c.id == participant_id)
        participant = await self.db.fetch_one(query)
        if participant:
            return self.parse_row(participant)

    async def update(self, participant):
        query = participants.update().where(participants.c.id == participant.get('id')).values(
            id=participant.get('id'),
            study_id=participant.get('study_id'),
            number=participant.get('number'),
            dominant_hand=participant.get('dominant_hand'),
            age=participant.get('age'),
            gender=participant.get('gender'),
            consent_video=participant.get('consent_video'),
        )
        await self.db.execute(query)

        participant = await self.get(participant.get('id'))
        await self.broadcast({
            'event': 'update',
            'entity': participant
        })
        return participant

    async def delete(self, participant_id):
        participant = await self.get(participant_id)

        query = participants.delete().where(participants.c.id == participant_id)
        await self.db.execute(query)

        await self.broadcast({
            'event': 'delete',
            'entity': participant
        })
        return participant


participant_controller = ParticipantsController()

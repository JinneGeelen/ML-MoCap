import logging
import sqlalchemy

from rx.subject import Subject

from db import metadata
from controllers.controller import Controller


logger = logging.getLogger()

cameras = sqlalchemy.Table('cameras', metadata,
                           sqlalchemy.Column(
                               'id', sqlalchemy.String, primary_key=True),
                           sqlalchemy.Column('name', sqlalchemy.String),
                           sqlalchemy.Column('location', sqlalchemy.String),
                           sqlalchemy.Column('online', sqlalchemy.Boolean),
                           sqlalchemy.Column('order', sqlalchemy.Integer),
                           )


class CameraController(Controller):
    camera_sockets = {}

    def parse_row(self, row):
        return {
            'id': row['id'],
            'name': row['name'],
            'location': row['location'],
            'online': row['online'],
            'order': row['order'],
        }

    async def connect(self, camera_id, websocket):
        self.camera_sockets[camera_id] = websocket

        camera = await self.get(camera_id)
        if not camera:
            camera = await self.create({
                'id': camera_id,
                'online': True,
                'order': 100
            })
        else:
            camera['online'] = True
            await self.update(camera)

    async def disconnect(self, camera_id):
        if camera_id in self.camera_sockets:
            del self.camera_sockets[camera_id]

        camera = await self.get(camera_id)
        if camera:
            camera['online'] = False
            await self.update(camera)

    async def reset_status(self):
        query = cameras.update().values(online=False)
        await self.db.execute(query)

    async def send_command(self, event, camera_ids=None):
        if camera_ids is None:
            camera_ids = self.camera_sockets.keys()

        logger.info('Sent command {} to cameras {}'.format(event, camera_ids))
        for key in camera_ids:
            if key in self.camera_sockets:
                await self.camera_sockets[key].send_json(event)

        return list(self.camera_sockets.keys())

    async def get_all(self):
        query = cameras.select()
        results = await self.db.fetch_all(query)
        return [self.parse_row(result) for result in results]

    async def create(self, camera):
        query = cameras.insert().values(
            id=camera.get('id'),
            name=camera.get('name'),
            location=camera.get('location'),
            online=camera.get('online'),
            order=camera.get('order')
        )
        await self.db.execute(query)

        entity = await self.get(camera.get('id'))
        await self.broadcast({
            'event': 'create',
            'entity': entity
        })
        return entity

    async def get(self, camera_id):
        query = cameras.select().where(cameras.c.id == camera_id)
        result = await self.db.fetch_one(query)
        if result:
            return self.parse_row(result)

    async def update(self, camera):
        query = cameras.update().where(cameras.c.id == camera.get('id')).values(
            id=camera.get('id'),
            name=camera.get('name'),
            location=camera.get('location'),
            online=camera.get('online'),
            order=camera.get('order')
        )
        await self.db.execute(query)

        entity = await self.get(camera.get('id'))
        await self.broadcast({
            'event': 'update',
            'entity': entity
        })
        return entity

    async def delete(self, camera_id):
        entity = await self.get(camera_id)

        query = cameras.delete().where(cameras.c.id == camera_id)
        await self.db.execute(query)

        await self.broadcast({
            'event': 'delete',
            'entity': entity
        })
        return entity


camera_controller = CameraController()

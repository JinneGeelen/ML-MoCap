import logging
import sqlalchemy

from starlette.applications import Starlette
from starlette.endpoints import WebSocketEndpoint
from starlette.responses import JSONResponse, PlainTextResponse

from db import get_db
from controllers import camera_controller as controller


logger = logging.getLogger()
api = Starlette()


@api.route('/', methods=['GET'])
async def get_all(request):
  return JSONResponse(await controller.get_all())


@api.route('/', methods=['POST'])
async def create(request):
  data = await request.json()
  entity = await controller.create(data)
  return JSONResponse(entity)


@api.route('/{id}', methods=['GET'])
async def read(request):
  entity_id = request.path_params.get('id')
  entity = await controller.get(entity_id)
  return JSONResponse(entity)


@api.route('/{id}', methods=['PUT'])
async def update(request):
  entity_id = request.path_params.get('id')
  data = await request.json()
  entity = await controller.update(data)
  return JSONResponse(entity)


@api.route('/{id}', methods=['DELETE'])
async def delete(request):
  entity_id = request.path_params.get('id')
  await controller.delete(entity_id)
  return PlainTextResponse('')


@api.websocket_route('/ws')
class WebsocketConnections(WebSocketEndpoint):
  encoding = 'json'

  async def on_connect(self, websocket):
    await controller.subscribe(websocket)
    await websocket.accept()
    logger.info('Frontent application subscribed to camera updates...')

  async def on_disconnect(self, websocket, close_code):
    await controller.unsubscribe(websocket)
    logger.info('Frontent application unsubscribed to camera updates...')


#websocket instead of http requests because it is much faster, keeps connection open between camera and controller 
@api.websocket_route('/connect/{id}')
class CameraConnections(WebSocketEndpoint):
  encoding = 'json'

  async def on_connect(self, websocket):
    entity_id = websocket.path_params.get('id')
    logger.info('Camera {} requesting to connect...'.format(entity_id))

    await controller.connect(entity_id, websocket)
    await websocket.accept()
    logger.info('Camera {} connected...'.format(entity_id))

  async def on_receive(self, websocket, message):
    if not 'event' in message:
      logger.error(
        'Received message from camera with no "event" in it...')
      await websocket.send_json({'error': 'no event name specified'})
      return

    event_method = 'on_{}'.format(message.get('event'))
    if not event_method in controller:
      logger.error(
        'Received message from camera with invalid event "{}"'.format(message.event))
      await websocket.send_json({'error': 'invalid event: {}'.format(message.event)})
      return

    controller[event_method](message.get('data'))

  async def on_disconnect(self, websocket, close_code):
    entity_id = websocket.path_params.get('id')

    logger.info('Camera {} disconnected...'.format(entity_id))

    await controller.disconnect(entity_id)

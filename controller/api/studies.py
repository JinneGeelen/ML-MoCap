import logging
import sqlalchemy

from starlette.applications import Starlette
from starlette.endpoints import WebSocketEndpoint
from starlette.responses import JSONResponse, PlainTextResponse

from db import get_db
from controllers import studies_controller as controller


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
    logger.info('Frontent application subscribed to studies updates...')

  async def on_disconnect(self, websocket, close_code):
    await controller.unsubscribe(websocket)
    logger.info('Frontent application unsubscribed to studies updates...')

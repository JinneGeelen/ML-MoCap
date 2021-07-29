import logging
import sqlalchemy

from starlette.applications import Starlette
from starlette.endpoints import WebSocketEndpoint
from starlette.responses import JSONResponse, PlainTextResponse

from db import get_db
from controllers import diagnostic_results_controller as controller


logger = logging.getLogger()
api = Starlette()

@api.route('/', methods=['GET'])
async def get_all(request):
  diagnostic_id = request.query_params.get('diagnostic_id')
  return JSONResponse(await controller.get_all(diagnostic_id))

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
    logger.info('Frontent application subscribed to diagnostic result updates...')

  async def on_disconnect(self, websocket, close_code):
    await controller.unsubscribe(websocket)
    logger.info('Frontent application unsubscribed to diagnostic result updates...')

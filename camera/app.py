import asyncio
import threading
import websockets
import os
import json
import logging
import signal
import time

from datetime import datetime, timedelta
from camera import CameraController

logging.basicConfig(level=logging.INFO)

camera_controller = CameraController()
logger = logging.getLogger()


class GracefulKiller:
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.kill_now = True


async def main():
    killer = GracefulKiller()

    camera_controller.start_uv4l()

    uri = 'ws://{}:3000/v1/cameras/connect/{}'.format(
        os.environ['CONTROLLER_HOST'], os.environ['ID'])
    async with websockets.connect(uri) as websocket:
        logger.info('Connected to {}'.format(uri))

        while not websocket.closed and not killer.kill_now:
            data = await websocket.recv()
            message = json.loads(data)

            if 'error' in message:
                logger.error(
                    "Error received from controller: {}".format(message['error']))
                continue

            if not 'event' in message:
                logger.error(
                    'Received message from controller with no "event" in it...')
                continue

            event_method = 'on_{}'.format(message.get('event'))
            logger.info("Received event {} with data {}".format(
                event_method, message.get('data')))

            threading.Thread(target=getattr(camera_controller, event_method),
                             args=[message.get('data')],
                             daemon=True).start()

        logger.info('Disconnected from websocket')
        await camera_controller.force_stop()


# Start the application
if __name__ == '__main__':
    logger.info('Starting event loop...')
    asyncio.run(main())

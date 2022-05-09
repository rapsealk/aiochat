import json
from datetime import datetime
from uuid import uuid4

from aiohttp import web

from aiochat.controllers.base import BaseController


class WebSocketController(BaseController):
    def __init__(self):
        self._websockets = []

    async def handle(self, request: web.Request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        uuid = str(uuid4())

        self._websockets.append(ws)

        async for message in ws:
            if message.data == 'close':
                await ws.close()
                break

            for websocket in self._websockets:
                await websocket.send_json({
                    'uuid': uuid,
                    'message': json.loads(message.data).get('message', ''),
                    'timestamp': datetime.now().isoformat()
                })

        cls._websockets.remove(ws)

        return ws

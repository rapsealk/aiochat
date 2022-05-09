import json
import os
from datetime import datetime
from uuid import uuid4

from aiohttp import web

STATIC_FILE_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..', 'static')
)


class WebSocketManager:
    websockets = []

    @classmethod
    async def handle_websocket_request(cls, request):
        print('WebSocket connection starting')
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        print('WebSocket connection ready!')

        cls.websockets.append(ws)

        uuid = str(uuid4())

        async for message in ws:
            print(message)
            if message.data == 'close':
                await ws.close()
                break

            for websocket in cls.websockets:
                await websocket.send_json({
                    'uuid': uuid,
                    'message': json.loads(message.data).get('message', ''),
                    'timestamp': datetime.now().isoformat()
                })

        cls.websockets.remove(ws)
        print('WebSocket connection closed')
        return ws


async def handle(request: web.Request):
    # TODO: Session
    return web.FileResponse(
        path=os.path.join(STATIC_FILE_PATH, 'index.html')
    )


app = web.Application()
app.add_routes([
    web.get('/', handle),
    web.get('/ws', WebSocketManager.handle_websocket_request),
    web.static('/static', STATIC_FILE_PATH)
])


if __name__ == '__main__':
    web.run_app(app)

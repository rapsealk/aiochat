import os

from aiohttp import web

from aiochat.controllers import ChatController, WebSocketController

STATIC_FILE_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..', 'static')
)


app = web.Application()
app.add_routes([
    web.get('/', ChatController(static_file_path=STATIC_FILE_PATH).handle),
    web.get('/ws', WebSocketController().handle),
    web.static('/static', STATIC_FILE_PATH)
])


if __name__ == '__main__':
    web.run_app(app)

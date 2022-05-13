import os

import jinja2
from aiohttp import web
from aiohttp_jinja2 import setup as setup_aiohttp_jinja2

from aiochat.controllers import ChatController, WebSocketController

STATIC_FILE_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..', 'static')
)
JINJA_TEMPLATE_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..', 'templates')
)


async def create_app() -> web.Application:
    app = web.Application()

    setup_aiohttp_jinja2(app, loader=jinja2.FileSystemLoader(JINJA_TEMPLATE_PATH))

    app.add_routes([
        web.get('/', ChatController()),
        web.get('/ws', WebSocketController()),
        web.static('/static', STATIC_FILE_PATH)
    ])
    return app


if __name__ == '__main__':
    app = create_app()
    web.run_app(app)

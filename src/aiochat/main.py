import os

# import aioredis
import jinja2
from aiohttp import web
from aiohttp_jinja2 import setup as setup_aiohttp_jinja2
# from aiohttp_session import setup as setup_aiohttp_session
# from aiohttp_session.redis_storage import RedisStorage

# from aiochat.common import REDIS_HOST
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

    # redis_pool = await aioredis.from_url(f'redis://{REDIS_HOST}', encoding='utf-8', decode_responses=True)
    # storage = RedisStorage(redis_pool=redis_pool)
    # setup_aiohttp_session(app, storage=storage)

    app.add_routes([
        web.get('/', ChatController()),
        web.get('/ws', WebSocketController()),
        web.static('/static', STATIC_FILE_PATH)
    ])
    return app


if __name__ == '__main__':
    app = create_app()
    web.run_app(app)

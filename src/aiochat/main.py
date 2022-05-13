import os

import aioredis
from aiohttp import web
from aiohttp_session import setup as setup_aiohttp_session
from aiohttp_session.redis_storage import RedisStorage

from aiochat.controllers import ChatController, WebSocketController

STATIC_FILE_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..', 'static')
)


async def create_app() -> web.Application:
    app = web.Application()

    redis_pool = await aioredis.from_url('redis://localhost', encoding='utf-8', decode_responses=True)
    storage = RedisStorage(redis_pool=redis_pool)
    setup_aiohttp_session(app, storage=storage)

    app.add_routes([
        web.get('/', ChatController(static_file_path=STATIC_FILE_PATH)),
        web.get('/ws', WebSocketController()),
        web.static('/static', STATIC_FILE_PATH)
    ])
    return app


if __name__ == '__main__':
    app = create_app()
    web.run_app(app)

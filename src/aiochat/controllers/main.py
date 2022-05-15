import aiohttp
import aiohttp_jinja2
import aioredis
from aiohttp import web

from aiochat.common import KEY_SESSION_UUID, REDIS_HOST
from aiochat.controllers.base import BaseController


class MainController(BaseController):
    async def __call__(self, request: web.Request):
        if not (cookie := request.cookies.get(KEY_SESSION_UUID)):
            raise aiohttp.web_exceptions.HTTPTemporaryRedirect(location='/join')
        redis = await aioredis.from_url(f'redis://{REDIS_HOST}', encoding='utf-8', decode_responses=True)
        if not await redis.get(cookie):
            raise aiohttp.web_exceptions.HTTPTemporaryRedirect(location='/join')
        response = aiohttp_jinja2.render_template('index.html', request, context={})
        response.set_cookie(KEY_SESSION_UUID, cookie)
        return response

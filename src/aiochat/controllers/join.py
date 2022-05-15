from uuid import uuid4

import aiohttp_jinja2
import aioredis
from aiohttp import web

from aiochat.common import KEY_SESSION_UUID, REDIS_HOST
from aiochat.controllers.base import BaseController


class JoinController(BaseController):
    async def __call__(self, request: web.Request):
        if request.method == 'GET':
            return await self._get_join_view(request)
        elif request.method == 'POST':
            return await self._post_user_to_join(request)

    async def _get_join_view(self, request: web.Request):
        return aiohttp_jinja2.render_template('join.html', request, context={})

    async def _post_user_to_join(self, request: web.Request):
        body = self._parse_query_to_dict(await request.text())
        cookie = str(uuid4())
        redis = await aioredis.from_url(f'redis://{REDIS_HOST}', encoding='utf-8', decode_responses=True)
        await redis.set(cookie, body.get('username'))
        response = web.HTTPSeeOther(location='/')
        response.set_cookie(KEY_SESSION_UUID, cookie)
        return response

    def _parse_query_to_dict(self, query: str):
        """Convert http querystring to dict.

        Args:
            query (str): A http querystring. (e.g. name=rapsealk&foo=bar&lorem=ipsum)

        Returns:
            A converted dict. (e.g. {"name": "rapsealk", "foo": "bar", "lorem": "ipsum"})
        """
        return dict(map(lambda x: x.split('='), query.split('&')))

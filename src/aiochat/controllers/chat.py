from uuid import uuid4

import aiohttp_jinja2
from aiohttp import web

from aiochat.common import KEY_SESSION_UUID
from aiochat.controllers.base import BaseController


class ChatController(BaseController):
    async def __call__(self, request: web.Request):
        session = request.cookies.get(KEY_SESSION_UUID, str(uuid4()))
        response = aiohttp_jinja2.render_template('index.html', request, context={})
        response.set_cookie(KEY_SESSION_UUID, session)
        return response

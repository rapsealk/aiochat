import os

from aiohttp import web

from aiochat.controllers.base import BaseController


class ChatController(BaseController):
    def __init__(self, static_file_path: str):
        self._static_file_path = static_file_path

    async def __call__(self, request: web.Request):
        return web.FileResponse(
           path=os.path.join(self._static_file_path, 'index.html')
        )

import abc

from aiohttp import web


class BaseController(abc.ABC):
    @abc.abstractmethod
    async def handle(self, request: web.Request):
        raise NotImplementedError()

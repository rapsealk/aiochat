import abc

from aiohttp import web


class BaseController(abc.ABC):
    @abc.abstractmethod
    async def __call__(self, request: web.Request):
        raise NotImplementedError()

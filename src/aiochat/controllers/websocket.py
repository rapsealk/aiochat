import asyncio
import json
import os
import time
from uuid import uuid4

import aioredis
from aiohttp import web

from aiochat.controllers.base import BaseController

REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_CHANNEL_ID = 'aiochat-channel'


class Message:
    def __init__(self, tag: str, uuid: str, message: str):
        self._tag = tag
        self._uuid = uuid
        self._message = message

    def json(self) -> str:
        return json.dumps({
            'tag': self._tag,
            'uuid': self._uuid,
            'message': self._message,
            'timestamp': time.time() * 1000,
            'pid': os.getpid()
        })


class WebSocketController(BaseController):
    async def handle(self, request: web.Request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        redis = await aioredis.from_url(f'redis://{REDIS_HOST}', encoding='utf-8', decode_responses=True)

        async def consume_message(channel: aioredis.client.PubSub, websocket: web.WebSocketResponse):
            await channel.subscribe(REDIS_CHANNEL_ID)
            while not websocket.closed:
                try:
                    if message := await channel.get_message(ignore_subscribe_messages=True, timeout=1.0):
                        await websocket.send_json(json.loads(message.get('data', '{}')))
                    await asyncio.sleep(0.01)
                except asyncio.TimeoutError:
                    pass
                except ConnectionResetError:
                    break
            await channel.unsubscribe(REDIS_CHANNEL_ID)

        future = asyncio.create_task(consume_message(redis.pubsub(), ws))

        uuid = str(uuid4())

        await redis.publish(
            REDIS_CHANNEL_ID,
            Message(tag='event', uuid=uuid, message=f'{uuid} has joined.').json()
        )

        async for message in ws:
            if ws.closed:
                break
            if message.data == 'close':
                await ws.close()
                break
            await redis.publish(
                REDIS_CHANNEL_ID,
                Message(tag='message', uuid=uuid, message=json.loads(message.data).get('message', '')).json()
            )

        await future

        await redis.publish(
            REDIS_CHANNEL_ID,
            Message(tag='event', uuid=uuid, message=f'{uuid} has left.').json()
        )
        await redis.close()

        return ws

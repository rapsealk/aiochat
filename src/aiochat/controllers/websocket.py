import asyncio
import json
import os
import time

import aioredis
from aiohttp import web

from aiochat.common import REDIS_HOST, REDIS_CHANNEL_ID
from aiochat.controllers.base import BaseController


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
    async def __call__(self, request: web.Request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        uuid = await ws.receive_str(timeout=None)

        redis = await aioredis.from_url(f'redis://{REDIS_HOST}', encoding='utf-8', decode_responses=True)
        await redis.publish(
            uuid,
            Message(tag='command', uuid=uuid, message='close').json()
        )

        future = asyncio.create_task(self._consume_message(redis.pubsub(), ws, uuid))

        username = await redis.get(uuid)

        await redis.publish(
            REDIS_CHANNEL_ID,
            Message(tag='event', uuid=username, message=f'{username} has joined.').json()
        )

        async for message in ws:
            if ws.closed:
                break
            if message.data == 'close':
                await ws.close()
                break
            await redis.publish(
                REDIS_CHANNEL_ID,
                Message(tag='message', uuid=username, message=json.loads(message.data).get('message', '')).json()
            )

        if not future.cancelled():
            future.cancel()

        await redis.publish(
            REDIS_CHANNEL_ID,
            Message(tag='event', uuid=uuid, message=f'{username} has left.').json()
        )
        await redis.close()

        return ws

    async def _consume_message(self, channel: aioredis.client.PubSub, websocket: web.WebSocketResponse, uuid: str):
        await channel.subscribe(REDIS_CHANNEL_ID, uuid)
        while not websocket.closed:
            try:
                if message := await channel.get_message(ignore_subscribe_messages=True, timeout=1.0):
                    if msg := json.loads(message.get('data', {})):
                        if msg.get('tag') == 'command' and msg.get('message') == 'close':
                            await websocket.close()
                            break
                    await websocket.send_json(json.loads(message.get('data', '{}')))
                await asyncio.sleep(0.01)
            except asyncio.TimeoutError:
                pass
            except ConnectionResetError:
                break
        await channel.unsubscribe(REDIS_CHANNEL_ID)

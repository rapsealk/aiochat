import asyncio
import json
import time
from uuid import uuid4

import aioredis
from aiohttp import web

from aiochat.controllers.base import BaseController

REDIS_CHANNEL_ID = 'aiochat-channel'


class WebSocketController(BaseController):
    async def handle(self, request: web.Request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        redis = await aioredis.from_url('redis://localhost', encoding='utf-8', decode_responses=True)

        async def consume_message(channel: aioredis.client.PubSub, websocket: web.WebSocketResponse):
            await channel.subscribe(REDIS_CHANNEL_ID)
            while not websocket.closed:
                try:
                    if message := await channel.get_message(ignore_subscribe_messages=True, timeout=1.0):
                        await websocket.send_json(json.loads(message.get('data', '{}')))
                    await asyncio.sleep(0.01)
                except asyncio.TimeoutError:
                    pass

        future = asyncio.create_task(consume_message(redis.pubsub(), ws))

        uuid = str(uuid4())

        async for message in ws:
            if message.data == 'close':
                await ws.close()
                break
            await redis.publish(REDIS_CHANNEL_ID, json.dumps({
                'uuid': uuid,
                'message': json.loads(message.data).get('message', ''),
                'timestamp': time.time() * 1000
            }))

        await future

        return ws

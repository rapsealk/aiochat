import os

KEY_SESSION_UUID = 'aiochat-uuid'

REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_CHANNEL_ID = 'aiochat-channel'

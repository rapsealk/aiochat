import os

from aiohttp import web

STATIC_FILE_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..', 'static')
)


async def handle(request: web.Request):
    # TODO: Session
    return web.FileResponse(
        path=os.path.join(STATIC_FILE_PATH, 'index.html')
    )


app = web.Application()
app.add_routes([
    web.get('/', handle),
])


if __name__ == '__main__':
    web.run_app(app)

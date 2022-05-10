FROM python:3.10.4-alpine3.15

ENV PYTHONUNBUFFERED=1
ENV REDIS_HOST=host.docker.internal
ENV PORT=8000

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
COPY ./requirements-dev.txt /app/requirements-dev.txt
COPY ./src /app/src
COPY ./static /app/static
COPY ./setup.py /app/setup.py
COPY ./gunicorn.conf.py /app/gunicorn.conf.py

RUN pip install --upgrade pip --no-cache-dir
RUN pip install -r requirements.txt --no-cache-dir
RUN pip install -e .

EXPOSE $PORT

ENTRYPOINT gunicorn src.aiochat.main:app

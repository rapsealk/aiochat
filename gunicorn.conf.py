import multiprocessing

host = '0.0.0.0'
port = 8000
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'aiohttp.GunicornWebWorker'

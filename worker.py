import os

import redis
# from redis import Redis

from rq import Worker, Queue, Connection

listen = ['dl']
# listen = ['high', 'default', 'low']

redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')

conn = redis.from_url(redis_url)
# conn = Redis()


if __name__ == '__main__':
    with Connection(connection=conn):
        worker = Worker(map(Queue, listen))
        worker.work()

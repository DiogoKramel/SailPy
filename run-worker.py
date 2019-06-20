import os
from redis import Redis
from rq import Worker, Queue, Connection

redis_url = os.environ.get('REDISCLOUD_URL', 'redis://localhost:6379')
redis = Redis()
conn = redis.from_url(redis_url)

listen = ['high', 'default', 'low']

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()
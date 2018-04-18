import redis
import time
from random import randint


SLEEP_TIME = 0.0002
QUEUE_NAME = 'test_bench.sha'
PRINT_NUMBER = False

redis_client = redis.StrictRedis()

while(True):
    number = randint(1, 9)
    if PRINT_NUMBER:
        print("Pushing number %i to queue %s" % (number, QUEUE_NAME))

    redis_client.rpush(QUEUE_NAME, number)

    if SLEEP_TIME > 0:
        time.sleep(SLEEP_TIME)

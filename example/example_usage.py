from wqueue import WQueue

from example.example_config import CONFIG

wqueue = WQueue(config=CONFIG)


@wqueue.listen_events("my.redis.queue")
def my_function(event):
    print(event)

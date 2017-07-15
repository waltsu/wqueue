import logging
from wqueue.redis_adapter import RedisAdapter

logging.basicConfig(level=logging.DEBUG)


class WQueue(object):
    def __init__(self):
        self.redis_adapter = RedisAdapter()

    def listen_events(self, queue_name):
        def function_wrapper(function):
            self.redis_adapter.register(queue_name, function)
        return function_wrapper

    def start(self):
        self.redis_adapter.start_listening()

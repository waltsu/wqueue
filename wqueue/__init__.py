import logging
from wqueue.config import merge_with_default_config


logging.basicConfig(level=logging.DEBUG)


class WQueue(object):
    def __init__(self, config=None):
        from wqueue.adapters.redis.adapter import RedisAdapter

        self.config = merge_with_default_config(config)

        self.redis_adapter = RedisAdapter(self.config)

    def listen_events(self, queue_name):
        def function_wrapper(function):
            self.redis_adapter.register(queue_name, function)
        return function_wrapper

    def start(self):
        self.redis_adapter.start_listening()

import logging
from wqueue.config import set_config


logging.basicConfig(level=logging.DEBUG)


class WQueue(object):
    def __init__(self, config=None):
        set_config(config)

        from wqueue.adapters.redis.adapter import RedisAdapter
        self.redis_adapter = RedisAdapter(self.config)

    def listen_events(self, queue_name):
        def function_wrapper(function):
            self.redis_adapter.register(queue_name, function)
        return function_wrapper

    def start(self):
        self.redis_adapter.start_listening()

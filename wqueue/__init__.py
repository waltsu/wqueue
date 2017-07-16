import logging

from queue import Queue

from wqueue.config import set_config
from wqueue.handlers.handler import Handler
from wqueue.adapters.redis_adapter import RedisAdapter


logging.basicConfig(level=logging.DEBUG)


class WQueue(object):
    def __init__(self, config=None):
        set_config(config)

        self.message_queue = Queue()

        self.adapter = RedisAdapter(self.message_queue)
        self.handler = Handler(self.message_queue)

    def listen_events(self, queue_name):
        def function_wrapper(function):
            self.adapter.register(queue_name, function)
            self.handler.add_function(queue_name, function)
        return function_wrapper

    def start(self):
        self.adapter.start_listening()
        self.handler.start()

from wqueue.redis_adapter import RedisAdapter


class WQueue(object):
    def __init__(self):
        self.redis_adapter = RedisAdapter()

    def listen_events(self, queue_name):
        def function_wrapper(function):
            self.redis_adapter.register(queue_name, function)
        return function_wrapper

from wqueue.handlers.multi_thread import MultiThreadHandler


class Handler(object):
    def __init__(self, message_queue):
        self.functions = {}
        self.message_queue = message_queue

        self.listener = None

    def add_function(self, queue_name, function):
        self.functions[queue_name] = function

    def start(self):
        self.listener = MultiThreadHandler(self.message_queue, self.functions)
        self.listener.start()

    def stop(self):
        self.listener.stop()

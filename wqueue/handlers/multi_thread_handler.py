import logging
import threading
import queue

from wqueue.config import get_config


logger = logging.getLogger(__name__)


class MultiThreadHandler(object):
    def __init__(self, message_queue, config=None):
        self.functions = {}
        self.is_running = False
        self.message_queue = message_queue

        if config is None:
            self.config = get_config()["handlers"]["multi_thread"]
        else:
            self.config = config

    def add_function(self, queue_name, function):
        self.functions[queue_name] = function

    def start(self):
        thread_count = self.config["thread_count"]
        threads = self._setup_threads(self.message_queue, self.functions, thread_count)

        logger.debug("Starting multi thread handler")
        self.is_running = True
        for thread in threads:
            thread.start()

    def stop(self):
        logger.debug("Stopping multi thread handler")
        self.is_running = False

    def _setup_threads(self, message_queue, functions, thread_count):
        logger.info("Setup %i threads" % thread_count)
        return [
            threading.Thread(target=self._read_queue, args=[message_queue, functions])
            for i in range(thread_count)
        ]

    def _read_queue(self, message_queue, functions):
        while self.is_running:
            try:
                event = message_queue.get(True, self.config["queue_listen_timeout"])
            except queue.Empty:
                event = None

            if event is not None and event.queue_name not in functions.keys():
                logger.error("Function not found for %s" % event.queue_name)
            elif event:
                function = functions[event.queue_name]
                try:
                    function(event.data)
                except Exception as exception:
                    logger.error(
                        "Function from queue %s raised exception %s" % (event.queue_name, exception)
                    )

import logging
import threading
import queue

from wqueue.config import get_config


logger = logging.getLogger(__name__)


class MultiThreadHandler(object):
    def __init__(self, message_queue, functions):
        self.config = get_config()["handlers"]["multi_thread"]
        self.is_running = False

        thread_count = self.config["thread_count"]
        logger.info("Initializing multi thread handler with %i threads" % thread_count)
        self.threads = self._setup_threads(message_queue, functions, thread_count)

    def start(self):
        logger.debug("Starting multi thread handler")
        self.is_running = True
        for thread in self.threads:
            thread.start()

    def stop(self):
        logger.debug("Stopping multi thread handler")
        self.is_running = False

    def _setup_threads(self, message_queue, functions, thread_count):
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
                function(event.data)

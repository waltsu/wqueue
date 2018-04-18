import logging
import threading
import queue
from concurrent.futures import ThreadPoolExecutor
from functools import partial

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
        logger.debug("Starting multi thread handler")
        self.is_running = True

        queue_listener_thread = self._setup_queue_listener_thread(
            self.message_queue, self.functions
        )
        queue_listener_thread.start()

    def stop(self):
        logger.debug("Stopping multi thread handler")
        self.is_running = False

    def _setup_queue_listener_thread(self, message_queue, functions):
        return threading.Thread(target=self._read_queue, args=[message_queue, functions])

    def _read_queue(self, message_queue, functions):
        thread_count = self.config["thread_count"]
        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            while self.is_running:
                event = self._read_event_from_queue(message_queue)
                if event and event.queue_name in functions.keys():
                    function = functions[event.queue_name]
                    executor.submit(
                        partial(self._execute_and_log_possible_exception, function, event.data)
                    )
                elif event is not None:
                    logger.error("Function not found for %s" % event.queue_name)

    def _read_event_from_queue(self, message_queue):
        try:
            event = message_queue.get(True, self.config["queue_listen_timeout"])
        except queue.Empty:
            event = None

        return event

    def _execute_and_log_possible_exception(self, function, argument):
        try:
            function(argument)
        except Exception as exception:
            logger.exception("Got exception when executing function %s" % function)

import logging
import threading
import queue

from wqueue.config import get_config


logger = logging.getLogger(__name__)


class BaseHandler(object):
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
        logger.debug("Starting handler %s", type(self).__name__)
        self.is_running = True

        queue_listener_thread = self._setup_queue_listener_thread(
            self.message_queue, self.functions
        )
        queue_listener_thread.start()

    def stop(self):
        logger.debug("Stopping handler %s", type(self).__name__)
        self.is_running = False

    def on_event(self, function, event):
        raise NotImplementedError("Subclasses should implement this method")

    def _setup_queue_listener_thread(self, message_queue, functions):
        return threading.Thread(target=self._read_queue, args=[message_queue, functions])

    def _read_queue(self, message_queue, functions):
        while self.is_running:
            event = self._read_event_from_queue(message_queue)
            if event and event.queue_name in functions.keys():
                function = functions[event.queue_name]
                self.on_event(function, event)
            elif event is not None:
                logger.error("Function not found for %s" % event.queue_name)

    def _read_event_from_queue(self, message_queue):
        try:
            event = message_queue.get(True, self.config["queue_listen_timeout"])
        except queue.Empty:
            event = None

        return event

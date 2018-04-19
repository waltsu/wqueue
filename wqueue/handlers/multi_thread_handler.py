import logging
from concurrent.futures import ThreadPoolExecutor
from functools import partial

from wqueue.handlers.base_handler import BaseHandler


logger = logging.getLogger(__name__)


class MultiThreadHandler(BaseHandler):
    def __init__(self, message_queue, config=None):
        super(MultiThreadHandler, self).__init__(message_queue, config)
        thread_count = self.config["handlers"]["multi_thread"]["thread_count"]
        self.executor = ThreadPoolExecutor(max_workers=thread_count)

    def stop(self):
        super(MultiThreadHandler, self).stop()
        self.executor.shutdown(wait=True)

    def on_event(self, function, event):
        self.executor.submit(
            partial(self._execute_and_log_possible_exception, function, event.data)
        )

    def _execute_and_log_possible_exception(self, function, argument):
        try:
            function(argument)
        except Exception as exception:
            logger.exception("Got exception when executing function %s" % function)

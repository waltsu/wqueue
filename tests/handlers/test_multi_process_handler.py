from queue import Queue
from unittest.mock import Mock

from wqueue.event import Event
from wqueue.handlers.multi_process_handler import MultiProcessHandler

from tests.wqueue_test_case import WQueueTestCase
from tests.helpers.wait import wait_until_success


class MultiProcessHandlerTestCase(WQueueTestCase):
    def test_executes_events(self):
        queue = Queue()
        handler_function = Mock()
        queue_name = 'queue'

        handler = MultiProcessHandler()

        event_count = 10
        for i in range(0, 10):
            queue.put_nowait(Event(queue_name, "some data"))

        try:
            handler.start()
            wait_until_success(lambda: self.assertEqual(handler_function.call_count, event_count))
        finally:
            handler.stop()

from unittest.mock import patch
from queue import Queue

from wqueue.handlers.handler import Handler

from tests.wqueue_test_case import WQueueTestCase


class HandlerTestCase(WQueueTestCase):
    def setUp(self):
        super().setUp()
        self.queue = Queue()

    def test_adds_function(self):
        handler = Handler(self.queue)
        handler.add_function("function", lambda x: x)

        self.assertEqual(len(handler.functions.keys()), 1)

    @patch('wqueue.handlers.multi_thread.MultiThreadHandler.start')
    def test_starts_multi_thread_handler(self, start_patch):
        handler = Handler(self.queue)
        handler.start()
        self.assertTrue(start_patch.call_count, 1)

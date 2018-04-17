import threading
from unittest.mock import Mock
from queue import Queue
from functools import partial

from wqueue.handlers.multi_thread_handler import MultiThreadHandler
from wqueue.event import Event
from wqueue.config import get_config

from tests.wqueue_test_case import WQueueTestCase
from tests.helpers.wait import wait_until_success


class MultiThreadHandlerTestCase(WQueueTestCase):
    def test_executes_events(self):
        queue = Queue()

        first_queue_mock = Mock()
        queue_name = "queue"

        multi_thread_handler = MultiThreadHandler(queue)
        multi_thread_handler.add_function(queue_name, first_queue_mock)

        event_count = 10
        for i in range(0, 10):
            queue.put_nowait(Event(queue_name, "some data"))

        try:
            multi_thread_handler.start()
            wait_until_success(lambda: self.assertEqual(first_queue_mock.call_count, event_count))

            thread_count = get_config()["handlers"]["multi_thread"]["thread_count"]
            self.assertTrue(threading.active_count() >= thread_count + 1)
        finally:
            multi_thread_handler.stop()

    def test_starts_multiple_threads(self):
        multi_thread_handler = MultiThreadHandler(Queue())
        multi_thread_handler.start()

        thread_count = get_config()["handlers"]["multi_thread"]["thread_count"]
        try:
            wait_until_success(lambda: self.assertTrue(threading.active_count() >= thread_count + 1))
        finally:
            multi_thread_handler.stop()

    def test_catch_all_errors_from_user_functions(self):
        def fail_if_one(callback, number):
            if number == 1:
                raise Exception("Boom!")
            callback()

        queue = Queue()
        queue_name = "queue"
        success_callback = Mock()

        handler_config = get_config()["handlers"]["multi_thread"]
        handler_config["thread_count"] = 1
        multi_thread_handler = MultiThreadHandler(queue, config=handler_config)
        multi_thread_handler.add_function(queue_name, partial(fail_if_one, success_callback))

        queue.put_nowait(Event(queue_name, 1))
        queue.put_nowait(Event(queue_name, 2))
        try:
            multi_thread_handler.start()
            wait_until_success(lambda: self.assertTrue(success_callback.called))
        finally:
            multi_thread_handler.stop()

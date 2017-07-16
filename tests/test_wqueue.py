import unittest

from wqueue import WQueue


class WqueueTestCase(unittest.TestCase):
    def test_listen_events_registers_handler(self):
        wqueue = WQueue()

        @wqueue.listen_events("my_queue")
        def test_handler(event):
            return "test_handler"

        self.assertEqual(len(wqueue.adapter.handlers), 1)

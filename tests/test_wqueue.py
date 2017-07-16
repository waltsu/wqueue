import unittest

from wqueue import WQueue


class WqueueTestCase(unittest.TestCase):
    def test_listen_events_registers_handler(self):
        wqueue = WQueue()

        @wqueue.listen_events("my_queue")
        def test_handler(event):
            return "test_handler"

        self.assertEqual(len(wqueue.redis_adapter.handlers), 1)
        handler = wqueue.redis_adapter.handlers[0]
        self.assertEqual(handler["queue_name"], "my_queue")

        self.assertIsNotNone(handler["worker"])

    def test_use_default_configs(self):
        wqueue = WQueue()
        self.assertEqual(wqueue.config["redis"]["port"], 6379)

    def test_override_default_config(self):
        config = {"redis": {"pop_timeout": 5}}
        wqueue = WQueue(config=config)
        self.assertEqual(wqueue.config["redis"]["pop_timeout"], 5)
        self.assertEqual(wqueue.config["redis"]["port"], 6379)

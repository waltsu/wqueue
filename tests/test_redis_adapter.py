import unittest
from unittest.mock import Mock

import redis

from wqueue.redis_adapter import RedisAdapter

from tests.helpers.wait import wait_until_success


class RedisAdapterTestCase(unittest.TestCase):
    def setUp(self):
        self.redis_client = redis.StrictRedis(host="localhost", port=6379)

    def test_starts_to_listen_queues(self):
        redis_adapter = RedisAdapter()
        mock = Mock()
        redis_adapter.register("my_queue", mock)

        try:
            redis_adapter.start_listening()

            self.redis_client.rpush("my_queue", 1, 2)
            wait_until_success(lambda: self.assertEqual(mock.call_count, 2))
        finally:
            redis_adapter.stop_listening()

    def test_can_listen_multiple_queues(self):
        redis_adapter = RedisAdapter()

        first_queue_mock = Mock()
        redis_adapter.register("first_queue", first_queue_mock)

        second_queue_mock = Mock()
        redis_adapter.register("second_queue", second_queue_mock)

        try:
            redis_adapter.start_listening()

            self.redis_client.rpush("first_queue", 1)
            self.redis_client.rpush("second_queue", 1)
            wait_until_success(lambda: self.assertTrue(first_queue_mock.called))
            wait_until_success(lambda: self.assertTrue(second_queue_mock.called))
        finally:
            redis_adapter.stop_listening()

import redis
from queue import Queue

from wqueue.adapters.redis_adapter import RedisAdapter

from tests.wqueue_test_case import WQueueTestCase
from tests.helpers.wait import wait_until_success


class RedisAdapterTestCase(WQueueTestCase):
    def setUp(self):
        super().setUp()
        self.redis_client = redis.StrictRedis(host="localhost", port=6379)

    def test_starts_to_listen_queues(self):
        message_queue = Queue()
        redis_adapter = RedisAdapter(message_queue)
        redis_adapter.register("my_queue", lambda x: x)

        try:
            redis_adapter.start_listening()

            self.redis_client.rpush("my_queue", 1, 2)
            wait_until_success(lambda: self.assertEqual(message_queue.qsize(), 2))
        finally:
            redis_adapter.stop_listening()

    def test_can_listen_multiple_queues(self):
        message_queue = Queue()
        redis_adapter = RedisAdapter(message_queue)

        redis_adapter.register("first_queue", lambda x: x)

        redis_adapter.register("second_queue", lambda x: x)

        try:
            redis_adapter.start_listening()

            self.redis_client.rpush("first_queue", 1)
            self.redis_client.rpush("second_queue", 1)
            wait_until_success(lambda: self.assertEqual(message_queue.qsize(), 2))
        finally:
            redis_adapter.stop_listening()

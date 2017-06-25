import unittest

from wqueue.redis_adapter import RedisAdapter

class RedisAdapterTestCase(unittest.TestCase):
  def test_starts_to_listen_queues(self):
    redis_adapter = RedisAdapter()
    redis_adapter.register("my_queue", lambda event: event)

    redis_adapter.listen() # Not implemented

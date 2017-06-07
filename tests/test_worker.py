import unittest
from unittest.mock import Mock

from tests.helpers.wait import wait_until_success
from wqueue.worker import Worker

class WorkerTestCase(unittest.TestCase):
  def test_worker_can_be_stopped(self):
    try:
      mock = Mock()
      worker = Worker(function=mock)
      worker.start()
      wait_until_success(lambda: self.assertTrue(mock.called))
    finally:
      worker.stop()

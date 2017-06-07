import unittest

from wqueue.worker import Worker

class WorkerTestCase(unittest.TestCase):
  def test_worker_can_be_stopped(self):
    worker = Worker()
    worker.start()
    worker.stop()

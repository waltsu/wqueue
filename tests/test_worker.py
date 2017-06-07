import unittest

from wqueue.worker import Worker

class WorkerTestCase(unittest.TestCase):
  def test_worker_starts(self):
    worker = Worker()
    worker.start()

import unittest
from unittest.mock import Mock

from tests.helpers.wait import wait_until_success
from wqueue.worker import Worker


class WorkerTestCase(unittest.TestCase):
    def test_worker_runs_function(self):
        try:
            mock = Mock()
            worker = Worker(function=mock)
            worker.start()
            wait_until_success(lambda: self.assertTrue(mock.called))
        finally:
            worker.stop()

    def test_run_two_workers_at_the_same_time(self):
        try:
            first_mock = Mock()
            second_mock = Mock()

            first_worker = Worker(function=first_mock)
            second_worker = Worker(function=second_mock)

            first_worker.start()
            second_worker.start()

            wait_until_success(lambda: self.assertTrue(first_mock.called))
            wait_until_success(lambda: self.assertTrue(second_mock.called))

        finally:
            first_worker.stop()
            second_worker.stop()

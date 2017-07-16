import unittest

from wqueue.config import set_config


class WQueueTestCase(unittest.TestCase):
    def setUp(self):
        set_config()

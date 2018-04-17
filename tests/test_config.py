import unittest

from wqueue import config
from wqueue.defaults import DEFAULTS


class ConfigTestCase(unittest.TestCase):
    def setUp(self):
        config._CONFIG = None

    def test_raises_error_if_config_not_set(self):
        with self.assertRaises(config.ConfigurationException):
            config.get_config()

    def test_sets_config(self):
        config.set_config({"extra_config": "foobar"})
        self.assertEqual(config.get_config()["extra_config"], "foobar")

    def test_merges_config_with_default_config(self):
        config.set_config({"handlers": {"multi_thread": {"thread_count": 10}}})

        multi_thread_config = config.get_config()["handlers"]["multi_thread"]
        self.assertEqual(multi_thread_config["thread_count"], 10)
        default_timeout = DEFAULTS["handlers"]["multi_thread"]["queue_listen_timeout"]
        self.assertEqual(multi_thread_config["queue_listen_timeout"], default_timeout)

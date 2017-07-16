import unittest

from wqueue import config


class ConfigTestCase(unittest.TestCase):
    def setUp(self):
        config._CONFIG = None

    def test_raises_error_if_config_not_set(self):
        with self.assertRaises(config.ConfigurationException):
            config.get_config()

    def test_sets_config(self):
        config.set_config({"extra_config": "foobar"})
        self.assertEqual(config.get_config()["extra_config"], "foobar")

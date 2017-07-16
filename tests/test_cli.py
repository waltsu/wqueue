import unittest
from unittest.mock import patch
from click.testing import CliRunner

from wqueue.cli import cli


class CLITestCase(unittest.TestCase):
    def test_worker_gives_error_if_application_import_fails(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['worker', '-a', 'foobar'])
        self.assertTrue(result.exit_code > 0)
        self.assertIn("Invalid value for --application", result.output)

    @patch('wqueue.WQueue.start')
    def test_starts_worker(self, start_patch):
        runner = CliRunner()
        result = runner.invoke(cli, ['worker', '-a', 'tests.fixtures.application_fixture'])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(start_patch.call_count, 1)

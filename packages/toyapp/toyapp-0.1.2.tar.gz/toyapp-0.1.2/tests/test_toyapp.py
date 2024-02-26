#!/usr/bin/env python

"""Tests for `toyapp` package."""


import unittest

from click.testing import CliRunner

from toyapp import cli, toyapp


class TestToyapp(unittest.TestCase):
    """Tests for `toyapp` package."""

    def setUp(self):
        """Set up test fixtures, if any."""
        self.num1 = "5.7"
        self.num2 = "3.2"
        self.operator = "+"
        self.answer = 8.9

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_001_addition_num1_num2_operator(self):
        """Test something."""
        assert toyapp.math_func(
            self.num1, self.num2, self.operator) == self.answer

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main, [self.num1, self.num2, self.operator])
        assert result.exit_code == 0
        assert "The answer to" in result.output
        help_result = runner.invoke(cli.main, ["--help"])
        assert help_result.exit_code == 0
        assert "--help  Show this message and exit." in help_result.output

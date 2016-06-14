#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_color_scheme_generator
----------------------------------

Tests for `color_scheme_generator` module.
"""


import sys
import unittest
import doctest
from contextlib import contextmanager
from click.testing import CliRunner

from color_scheme_generator import color_scheme_generator
from color_scheme_generator import cli
from color_scheme_generator import utils


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(utils))
    tests.addTests(doctest.DocTestSuite(color_scheme_generator))
    return tests


class TestColor_scheme_generator(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_000_something(self):
        pass

    def test_command_line_interface(self):
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'color_scheme_generator.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output


if __name__ == '__main__':
    sys.exit(unittest.main())

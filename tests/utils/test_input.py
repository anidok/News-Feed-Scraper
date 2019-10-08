import unittest
import argparse
from mockito import mock, unstub, verify, kwargs, when
from src.scraper.utils.input import NewsFeedInputHandler


class TestInputHandler(unittest.TestCase):

    def setUp(self):
        self.parser = mock()
        when(argparse).ArgumentParser().thenReturn(self.parser)
        when(self.parser).create_args_dict()

    def test_input_handler_parses_arguments(self):
        handler = NewsFeedInputHandler(self.parser)
        handler.parse_arguements()

        verify(self.parser).add_argument('--root_dir', **kwargs)
        verify(self.parser).add_argument('--source_list', **kwargs)

    def tearDown(self):
        unstub()

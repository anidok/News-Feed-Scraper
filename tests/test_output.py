import unittest
import json
from datetime import datetime
from mockito import mock, unstub, verify, ANY
from tests import datetime_converter
from src.output import JsonObjectOutputHandler


class TestOutput(unittest.TestCase):

    def setUp(self):
        self.mock_file_writer = mock()
        self.mock_mongo_connection = mock()

    def test_csv_output_writer(self):
        output_root_dir = 'F:/Test'
        target = JsonObjectOutputHandler(output_root_dir, self.mock_mongo_connection, self.mock_file_writer)

        source = 'cnn'
        publish_date = datetime.now()
        # publish_date_str = publish_date.strftime('%Y-%m-%dT%H.%M.%S')
        article = {}
        article['source'] = source
        article['publish_date'] = publish_date
        article_str = json.dumps(article, default=datetime_converter)

        target.accept(article, article_str)
        verify(self.mock_file_writer).write(ANY, article_str)
        verify(self.mock_mongo_connection).insert_one(article, 'articles')

    def tearDown(self):
        unstub()

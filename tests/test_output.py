import unittest
import json
from datetime import datetime, date
from mockito import mock, unstub, verify, ANY
from tests import datetime_converter
from src.scraper.output import JsonObjectOutputHandler


class TestOutput(unittest.TestCase):

    def setUp(self):
        self.mock_file_writer = mock()
        self.mock_mongo_connection = mock()

    def test_csv_output_writer(self):
        output_root_dir = 'F:/Test'
        target = JsonObjectOutputHandler(output_root_dir, self.mock_mongo_connection, self.mock_file_writer)

        article = {}
        article['source'] = 'cnn'
        article['title'] = 'some title'
        article['publish_datetime'] = datetime.now()
        article['publish_date'] = date.today()
        article_str = json.dumps(article, default=datetime_converter)

        target.accept(article, article_str)
        verify(self.mock_file_writer).write(ANY, article_str)
        verify(self.mock_mongo_connection).insert_one(article, 'articles')
        verify(self.mock_mongo_connection).is_document_present(ANY, 'articles')

    def tearDown(self):
        unstub()

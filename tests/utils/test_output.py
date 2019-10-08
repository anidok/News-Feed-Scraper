import unittest
import json
from datetime import datetime, date
from mockito import mock, unstub, verify, ANY, when
from tests import datetime_converter
from src.scraper.utils.output import JsonObjectOutputHandler


class TestOutput(unittest.TestCase):

    def setUp(self):
        self.mock_file_writer = mock()
        self.mock_mongo_connection = mock()

    def test_json_output_handler_inserts_document(self):
        output_root_dir = 'F:/Test'
        target = JsonObjectOutputHandler(output_root_dir, self.mock_mongo_connection, self.mock_file_writer)

        article = self.create_article()
        article_str = json.dumps(article, default=datetime_converter)

        target.accept(article, article_str)
        verify(self.mock_file_writer).write(ANY, article_str)
        verify(self.mock_mongo_connection).insert_one(article, 'articles')
        verify(self.mock_mongo_connection).is_document_present(ANY, 'articles')

    def test_json_output_handler_skips_duplicate_document(self):
        output_root_dir = 'F:/Test'
        target = JsonObjectOutputHandler(output_root_dir, self.mock_mongo_connection, self.mock_file_writer)
        when(self.mock_mongo_connection).is_document_present(ANY, ANY).thenReturn(True)

        article = self.create_article()
        article_str = json.dumps(article, default=datetime_converter)

        target.accept(article, article_str)

        verify(self.mock_mongo_connection, times=0).insert_one(ANY, ANY)

    @staticmethod
    def create_article():
        article = {}
        article['source'] = 'cnn'
        article['title'] = 'some title'
        article['publish_datetime'] = datetime.now()
        article['publish_date'] = date.today()
        return article

    def tearDown(self):
        unstub()

import unittest
from datetime import datetime
from newspaper import Article
from mockito import mock, unstub, verify, kwargs, when
from src.scraper.news_article import NewsArticle
from src.scraper.datetime_provider import DateTimeProvider


class TestNewsArticle(unittest.TestCase):

    def setUp(self):
        self.datetime_provider = mock(DateTimeProvider)
        self.now = datetime.now()
        when(self.datetime_provider).get_current_datetime().thenReturn(self.now)
        self.create_mock_source_article()
        when(self.source_article).parse()
        when(self.source_article).nlp()

    def test_input_handler_parses_arguments(self):
        news_article = NewsArticle(url='someurl', source='somesource', datetime_provider=self.datetime_provider, source_article=self.source_article)

        news_article.build()
        news_article_output = news_article.output_obj()

        verify(self.source_article).parse()
        verify(self.source_article).nlp()        
        self.assert_output(self.source_article, news_article_output)     

    def create_mock_source_article(self):
        self.source_article = mock(Article)
        self.source_article.authors = ['someauthor']
        self.source_article.title = 'sometitle'
        self.source_article.text = 'somebody'
        self.source_article.keywords = ['sometopic']
        self.source_article.publish_date = self.now

    def assert_output(self, expected: Article, actual: NewsArticle):
        self.assertEqual(expected.authors, actual['authors'])
        self.assertEqual(expected.text, actual['body'])
        self.assertEqual(expected.title, actual['title'])
        self.assertEqual(expected.keywords, actual['topics'])
        self.assertEqual('somesource', actual['source'])
        self.assertEqual(self.now, actual['publish_datetime'])
        self.assertEqual(self.now, actual['current_date'])

    def tearDown(self):
        unstub()

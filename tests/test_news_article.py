import unittest
from datetime import datetime
from newspaper import Article
from mockito import mock, unstub, verify, when
from src.scraper.news_article import NewsArticle
from src.scraper.utils.datetime_provider import DateTimeProvider


class TestNewsArticle(unittest.TestCase):

    def setUp(self):
        self.datetime_provider = mock(DateTimeProvider)
        self.now = datetime.now()
        when(self.datetime_provider).get_current_datetime().thenReturn(self.now)
        self.source_article = self.create_mock_source_article()
        when(self.source_article).parse()
        when(self.source_article).nlp()

    def test_news_article_parses_with_success(self):
        news_article = NewsArticle(url='someurl', source='somesource', datetime_provider=self.datetime_provider, source_article=self.source_article)

        news_article.build()
        news_article_output = news_article.output_obj()

        verify(self.source_article).parse()
        verify(self.source_article).nlp()
        self.assert_output(self.source_article, news_article_output)

    def create_mock_source_article(self):
        source_article = mock(Article)
        source_article.authors = ['someauthor']
        source_article.title = 'sometitle'
        source_article.text = 'somebody'
        source_article.keywords = ['sometopic']
        source_article.publish_date = self.now

        return source_article

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

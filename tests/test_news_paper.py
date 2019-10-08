import unittest
from datetime import datetime
from typing import List
from newspaper import Article
from mockito import mock, unstub, verify, when, ANY
from src.scraper.news_paper import NewsPaper
from src.scraper.utils.datetime_provider import DateTimeProvider
from src.scraper.models.article_error_log import ArticleErrorLog
from src.scraper.utils.output import JsonObjectOutputHandler


class TestNewsArticle(unittest.TestCase):

    def setUp(self):
        self.datetime_provider = mock(DateTimeProvider)
        self.json_object_output_handler = mock(JsonObjectOutputHandler)
        self.paper = mock()
        self.error_logs: List[ArticleErrorLog] = []
        self.now = datetime.now()

        source_article = self.create_mock_source_article()
        self.articles: List[Article] = []
        self.articles.append(source_article)

        when(self.datetime_provider).get_current_datetime().thenReturn(self.now)

        for article in self.articles:
            when(article).parse()
            when(article).nlp()

    def test_news_paper_process_articles(self):
        when(self.json_object_output_handler).accept(ANY, ANY)

        news_paper = NewsPaper('someurl', self.datetime_provider, self.json_object_output_handler, self.error_logs, self.paper)
        news_paper.articles = self.articles
        news_paper.process_articles()

        verify(self.json_object_output_handler, times=1).accept(ANY, ANY)
        for article in self.articles:
            verify(article).parse()
            verify(article).nlp()

    def test_news_paper_add_error_logs(self):
        news_paper = NewsPaper('someurl', self.datetime_provider, self.json_object_output_handler, self.error_logs, self.paper)
        news_paper.articles = self.articles
        news_paper.process_articles()

        when(self.json_object_output_handler).accept(ANY, ANY).thenRaise(Exception)
        self.assertEqual(1, len(self.error_logs))

    def create_mock_source_article(self):
        source_article = mock(Article)
        source_article.authors = ['someauthor']
        source_article.title = 'sometitle'
        source_article.text = 'somebody'
        source_article.keywords = ['sometopic']
        source_article.publish_date = self.now

        return source_article

    def tearDown(self):
        unstub()

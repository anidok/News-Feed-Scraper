import traceback
from typing import List
import newspaper
from .news_article import NewsArticle
from .utils.output import JsonObjectOutputHandler
from .models.article_error_log import ArticleErrorLog
from .utils.datetime_provider import DateTimeProvider


class NewsPaper:
    # pylint: disable=too-many-instance-attributes,too-many-arguments
    def __init__(self, url, datetime_provider: DateTimeProvider, json_object_output_handler: JsonObjectOutputHandler,
                 error_logs: List[ArticleErrorLog], paper=None, memoize_articles: bool = True):
        self.brand = None
        self.articles: List = []
        self.article_count = None

        self.datetime_provider = datetime_provider
        self.json_object_output_handler = json_object_output_handler
        self.url = url
        self.error_logs = error_logs
        self.memoize_articles = memoize_articles
        self.paper = paper if paper is not None else newspaper.build(self.url, memoize_articles=self.memoize_articles)

    def process_articles(self):
        for article in self.articles:
            try:
                news_article = NewsArticle(url=self.url, source=self.brand, datetime_provider=self.datetime_provider, source_article=article)
                news_article.build()

                json_obj = news_article.output_obj()
                json_str = news_article.serialize()
                self.json_object_output_handler.accept(json_obj, json_str)

            # pylint: disable=broad-except
            except Exception:
                exception_traceback = traceback.format_exc()
                self.add_error_log(self.url, self.brand, exception_traceback)

    def add_error_log(self, url, source, message):
        error_log = ArticleErrorLog(url, source, message)
        self.error_logs.append(error_log)

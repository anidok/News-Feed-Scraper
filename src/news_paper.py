import logging
from typing import List
import newspaper
from news_article import NewsArticle
from output import JsonObjectOutputHandler
from article_error_log import ArticleErrorLog


class NewsPaper:
    # pylint: disable=too-many-instance-attributes
    def __init__(self, url, json_object_output_handler: JsonObjectOutputHandler, error_logs: List[ArticleErrorLog], memoize_articles: bool = False):
        self.brand = None
        self.articles: List = []
        self.article_count = None

        self.json_object_output_handler = json_object_output_handler
        self.url = url
        self.error_logs = error_logs
        self.memoize_articles = memoize_articles
        self.paper = newspaper.build(self.url, memoize_articles=self.memoize_articles)

    def process_articles(self):
        for article in self.articles:
            try:
                news_article = NewsArticle(url=self.url, source=self.brand, source_article=article)
                news_article.build()

                json_obj = news_article.output_obj()
                json_str = news_article.serialize()
                self.json_object_output_handler.accept(json_obj, json_str)

            # pylint: disable=broad-except
            except Exception as exception:
                logging.exception("Error occured while parsing article.", exc_info=exception)
                self.add_error_log(self.url, self.brand, exception)

    def add_error_log(self, url, source, message):
        error_log = ArticleErrorLog(url, source, message)
        self.error_logs.append(error_log)

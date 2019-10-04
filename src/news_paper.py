from typing import List
import newspaper
from news_article import NewsArticle
from output import JsonObjectOutputHandler


class NewsPaper:
    def __init__(self, url, json_object_output_handler: JsonObjectOutputHandler, memoize_articles: bool = False):
        self.brand = None
        self.articles: List = []
        self.article_count = None

        self.json_object_output_handler = json_object_output_handler
        self.url = url
        self.memoize_articles = memoize_articles
        self.paper = newspaper.build(self.url, memoize_articles=self.memoize_articles)

    def process_articles(self):
        for article in self.articles:
            news_article = NewsArticle(url=self.url, source=self.brand, source_article=article)
            news_article.build()

            json_obj = news_article.output_obj()
            json_str = news_article.serialize()
            self.json_object_output_handler.accept(json_obj, json_str)

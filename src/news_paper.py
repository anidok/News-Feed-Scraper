import newspaper
from news_article import NewsArticle

class NewsPaper:
    def __init__(self, url, memoize_articles: bool=False):
        self.brand = None
        self.articles: list = None
        self.article_count = None

        self.url = url
        self.memoize_articles = memoize_articles
        self.paper = newspaper.build(self.url, memoize_articles=self.memoize_articles)

    def process_articles(self):
        for article in self.articles:
            news_article = NewsArticle(url=self.url, source=self.brand, source_article=article)
            news_article.build()
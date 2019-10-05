import logging
from datetime import datetime
from typing import List
from newspaper import news_pool
from news_paper import NewsPaper


class NewsFeed:
    THREADS_PER_NEWS_SOURCE = 10

    def __init__(self, papers: List[NewsPaper] = None):
        self.newspapers = papers if papers is not None else []

    def add_newspaper(self, paper):
        self.newspapers.append(paper)

    def newspaper_count(self) -> int:
        return len(self.newspapers)

    def build(self):
        self.download_all_articles()
        self.populate_attributes_to_newspapers()
        self.process_all_newspaper_articles()

    def download_all_articles(self):
        papers = self.create_source_feed_list()
        news_pool.set(papers, threads_per_source=self.THREADS_PER_NEWS_SOURCE)
        news_pool.join()
        logging.info("Downloaded all news articles.")
        logging.info(datetime.now())

    def create_source_feed_list(self):
        papers = []
        for news_paper in self.newspapers:
            papers.append(news_paper.paper)

        return papers

    def populate_attributes_to_newspapers(self):
        for news_paper in self.newspapers:
            news_paper.brand = news_paper.paper.brand
            news_paper.articles = news_paper.paper.articles
            news_paper.article_count = len(news_paper.articles)

    def process_all_newspaper_articles(self):
        for newspaper in self.newspapers:
            newspaper.process_articles()

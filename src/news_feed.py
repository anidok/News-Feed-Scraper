from news_paper import NewsPaper
from newspaper import news_pool

class NewsFeed:
    def __init__(self, papers: list):
        self.newspapers: list[NewsPaper] = papers

    def add_newspaper(self, paper):
        self.newspapers.append(paper)

    def newspaper_count(self) -> int:
        return len(self.newspapers)

    def build(self):
        self.download_all_articles()
        self.populate_attributes_to_newspapers()

    def download_all_articles(self):
        papers = self.create_source_feed_list()
        news_pool.set(papers, threads_per_source=2)
        news_pool.join()

    def create_source_feed_list(self):
        papers = []
        for news_paper in self.newspapers:
            papers.append(news_paper.paper)

        return papers

    def populate_attributes_to_newspapers(self):
        for news_paper in self.newspapers:
            news_paper.brand = news_paper.paper.brand
            news_paper.articles = news_paper.paper.articles
            news_paper.article_count = news_paper.articles.count

    def process_all_newspaper_articles(self):
        for newspaper in self.newspapers:
            newspaper.process_articles()

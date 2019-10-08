import logging
from datetime import datetime
from typing import List
from newspaper import news_pool
from .news_paper import NewsPaper
from .article_error_log import ArticleErrorLog
from .datetime_provider import DateTimeProvider


class NewsFeed:
    THREADS_PER_NEWS_SOURCE = 10
    SUMMARY_FILE = 'summary.txt'
    ERROR_LOG_FILE = 'error_logs.txt'
    DEFAULT_OUTPUT_DIR = '.'

    def __init__(self, datetime_provider: DateTimeProvider, error_logs: List[ArticleErrorLog], papers: List[NewsPaper] = None, output_root_dir=None):
        self.newspapers = papers if papers is not None else []
        self.output_root_dir = output_root_dir if output_root_dir is not None else self.DEFAULT_OUTPUT_DIR
        self.error_logs = error_logs
        self.datetime_provider = datetime_provider

    def add_newspaper(self, paper):
        self.newspapers.append(paper)

    def newspaper_count(self) -> int:
        return len(self.newspapers)

    def build(self):
        self.download_all_articles()
        self.populate_attributes_to_newspapers()
        self.process_all_newspaper_articles()
        self.summarize_articles()
        self.generate_error_logs(self.output_root_dir)

    def download_all_articles(self):
        logging.info("Downloading all articles...")

        papers = self.create_source_feed_list()

        news_pool.set(papers, threads_per_source=self.THREADS_PER_NEWS_SOURCE)

        # Download feed from all sources in parallel threads
        news_pool.join()

        logging.info("Download complete.")
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
        logging.info("Processing all articles..")
        for newspaper in self.newspapers:
            newspaper.process_articles()
        logging.info("Processed all articles.")

    def summarize_articles(self):
        dir_suffix = self.datetime_provider.get_current_date_formatted_string()
        summary_file_path = self.output_root_dir + '/' + dir_suffix + '/' + self.SUMMARY_FILE
        error_count = len(self.error_logs)

        file = open(summary_file_path, 'w')
        for news_paper in self.newspapers:
            file.write("{0} - {1}\n".format(news_paper.brand, news_paper.article_count))
        file.write("Parsing Errors - {0}\n".format(error_count))
        file.close()

        logging.info('Stored download summary to %s', self.SUMMARY_FILE)

    def generate_error_logs(self, output_root_dir):
        dir_suffix = self.datetime_provider.get_current_date_formatted_string()
        error_log_file_path = output_root_dir + '/' + dir_suffix + '/' + self.ERROR_LOG_FILE

        with open(error_log_file_path, 'w') as file:
            for error_log in self.error_logs:
                file.write("{0}|{1}|{2}\n".format(error_log.url, error_log.source, error_log.error_message))

        logging.info('Created error log file.')
        logging.info("Errored out articles count: %d", len(self.error_logs))

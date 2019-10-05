import os
import logging
from datetime import datetime
from typing import List
from input import NewsFeedInputHandler
from output import JsonObjectOutputHandler
from news_paper import NewsPaper
from news_feed import NewsFeed
from article_error_log import ArticleErrorLog


class NewsApp:
    DEFAULT_LOG_LEVEL = 'INFO'

    def __init__(self):
        self.error_logs: List[ArticleErrorLog] = []

    def accept(self):
        self.apply_logging_level()

        start_time = datetime.now()
        logging.info("Start Time: %s", start_time)
        logging.info('Started scraping from all sources.')

        try:
            news_feed_input_handler = NewsFeedInputHandler()
            args_map = news_feed_input_handler.fetch_arguments()

            root_dir = args_map['root_dir']
            source_list = news_feed_input_handler.get_all_sources()
            json_object_output_handler = JsonObjectOutputHandler(output_root_dir=root_dir)

            papers = self.create_newspaper_objects(source_list, json_object_output_handler)

            news_feed = NewsFeed(papers)
            news_feed.build()

            logging.info('Scraping completed successfully.')
            logging.info("Errored out articles count: %d", len(self.error_logs))


            end_time = datetime.now()
            logging.info("End Time: %s", end_time)

            elapsed = (end_time - start_time).seconds
            logging.info("Total elapsed time: %s", elapsed)

        # pylint: disable=broad-except
        except Exception as exception:
            logging.exception("Error occured during scraping ", exc_info=exception)

            elapsed = (end_time - start_time).seconds
            logging.info("Total elapsed time: %s", elapsed)

    @classmethod
    def apply_logging_level(cls):
        logger = logging.getLogger()
        logger.setLevel(cls.get_logging_level())

    @classmethod
    def get_logging_level(cls):
        log_level_env = os.environ.get('LOGLEVEL')

        if log_level_env is None:
            return cls.DEFAULT_LOG_LEVEL

        return log_level_env

    def create_newspaper_objects(self, source_list, json_object_output_handler):
        papers: List[NewsPaper] = []
        for source in source_list:
            papers.append(NewsPaper(source, json_object_output_handler, self.error_logs))

        return papers

from typing import List
from input import NewsFeedInputHandler
from output import JsonObjectOutputHandler
from news_paper import NewsPaper
from news_feed import NewsFeed

class NewsApp:
    def __init__(self):
        pass

    def accept(self):
        news_feed_input_handler = NewsFeedInputHandler()        
        args_map = news_feed_input_handler.fetch_arguments()

        root_dir = args_map['root_dir']
        source_list = news_feed_input_handler.get_all_sources()
        json_object_output_handler = JsonObjectOutputHandler(output_root_dir=root_dir)

        papers = self.create_newspaper_objects(source_list, json_object_output_handler)

        news_feed = NewsFeed(papers)
        news_feed.build()

    @staticmethod
    def create_newspaper_objects(source_list, json_object_output_handler):
        papers: List[NewsPaper] = []
        for source in source_list:
            papers.append(NewsPaper(source, json_object_output_handler))

        return papers


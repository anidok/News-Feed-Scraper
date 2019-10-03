from model import Model
from datetime import datetime
from json_pickle_decimal import JsonPickleDecimal

class NewsArticle(Model):
    OUTPUT_ATTRS = ['authors', 'source', 'current_date', 'publish_date', 'title', 'body' 'topics']


    def __init__(self, *initial_data, **kwargs):
        self.url = None
        self.source = None
        self.source_article = None

        self.authors = None
        self.current_date = None
        self.publish_date = None
        self.title = None
        self.body = None
        self.category = None
        self.topics = None        
        
        super().__init__(*initial_data, **kwargs)

    def serialize(self) -> str:
        return JsonPickleDecimal.encode(self.output_obj())

    def output_obj(self):
        values = {}
        for attr in dir(self):
            if attr in self.OUTPUT_ATTRS:
                val = self.__getattribute__(attr)
                values[attr] = val

        return values

    def build(self):
        self.source_article.parse()
        self.source_article.nlp()
        self.populate_attributes_from_newspaper_article(self.source_article)

    def populate_attributes_from_newspaper_article(self, article):
        self.authors = article.authors
        self.publish_date = article.publish_date
        self.current_date = datetime.now()
        self.title = article.title
        self.body = article.text
        self.topics = article.keywords

    
from .models.model import Model
from .utils.json_pickle_decimal import JsonPickleDecimal
from .utils.datetime_provider import DateTimeProvider


# pylint: disable=too-many-instance-attributes
class NewsArticle(Model):
    OUTPUT_ATTRS = ['authors', 'source', 'current_date', 'publish_date', 'publish_time', 'publish_datetime', 'title', 'body', 'topics']
    DATE_FORMAT = '%Y-%m-%d'
    TIME_FORMAT = '%H:%M:%S'

    def __init__(self, *initial_data, **kwargs):
        self.url = None
        self.source = None
        self.source_article = None
        self.datetime_provider: DateTimeProvider = None

        self.authors = None
        self.current_date = None
        self.publish_date = None
        self.publish_time = None
        self.publish_datetime = None
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
        # Parse Article object from newspaper library and use it to populate attributes
        self.source_article.parse()
        self.source_article.nlp()
        self.populate_attributes_from_newspaper_article(self.source_article)

    def populate_attributes_from_newspaper_article(self, article):
        self.authors = article.authors
        self.current_date = self.datetime_provider.get_current_datetime()
        self.title = article.title
        self.body = article.text
        self.topics = article.keywords
        self.populate_datetime_attributes(article.publish_date)

    def populate_datetime_attributes(self, publish_date):
        self.publish_datetime = publish_date
        self.publish_date = publish_date.strftime(self.DATE_FORMAT)
        self.publish_time = publish_date.strftime(self.TIME_FORMAT)

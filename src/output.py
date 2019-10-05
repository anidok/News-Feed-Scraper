import os
import abc
from datetime import date
from .mongo_connection import MongoConnection


class FileWriter:
    @staticmethod
    def write(filename, data):
        with open(filename, 'w') as f:
            f.write(data)


class OutputHandler(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def accept(self, json_obj, json_str):
        raise NotImplementedError


class JsonObjectOutputHandler(OutputHandler):
    MONGO_COLLECTION = 'articles'

    def __init__(self, output_root_dir=None, mongo_connection: MongoConnection = None, file_writer: FileWriter = None, object_name_generator=None):
        self.output_root_dir = output_root_dir
        self.mongo_connection = mongo_connection

        if object_name_generator is None:
            object_name_generator = NewsArticleJsonObjectNameGenerator(self.output_root_dir)

        self.object_name_generator = object_name_generator
        self.file_writer = file_writer if file_writer is not None else FileWriter()

    def accept(self, json_obj, json_str):
        file_name = self.object_name_generator.format_filename(json_obj)
        self.file_writer.write(file_name, json_str)
        self.mongo_connection.insert_one(json_obj, self.MONGO_COLLECTION)


class JsonObjectNameGenerator(metaclass=abc.ABCMeta):
    SUFFIX = '.json'

    def __init__(self, output_root_dir=None):
        if output_root_dir is None:
            self.output_root_dir = '.'
        else:
            self.output_root_dir = output_root_dir
        self.output_dir = self.create_output_directory()

    def create_output_directory(self):
        today = date.today()
        dir_suffix = today.strftime("%Y-%m-%d")
        output_dir = "{0}/{1}/".format(self.output_root_dir, dir_suffix)

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        return output_dir

    @abc.abstractmethod
    def format_filename(self, json_obj):
        return NotImplementedError


class NewsArticleJsonObjectNameGenerator(JsonObjectNameGenerator):
    DATE_FORMAT = '%Y-%m-%dT%H.%M.%S'

    def format_filename(self, json_obj):
        source = json_obj['source']
        publish_date = json_obj['publish_date']
        publish_date = self.date_to_string(publish_date)

        filename = "{0}{1}_{2}{3}".format(self.output_dir, source, publish_date, self.SUFFIX)
        return filename

    def date_to_string(self, publish_date):
        return publish_date.strftime(self.DATE_FORMAT)

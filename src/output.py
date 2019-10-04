import os
import abc
from datetime import date

class OutputHandler:
    def accept(self, rows):
        raise NotImplementedError

    def close(self):
        pass

class JsonObjectOutputHandler(OutputHandler):
    def __init__(self, output_root_dir=None, object_name_generator=None):
        self.output_root_dir = output_root_dir

        if object_name_generator is None:
            object_name_generator = NewsArticleJsonObjectNameGenerator(self.output_root_dir)

        self.object_name_generator = object_name_generator


    def accept(self, json_obj, json_str):
        file_name = self.object_name_generator.format_filename(json_obj)
        with open(file_name, 'w') as f:
            f.write(json_str)


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
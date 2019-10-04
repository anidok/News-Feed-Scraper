import argparse
import abc


class InputHandler(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def parse_arguements(self):
        raise NotImplementedError


class NewsFeedInputHandler(InputHandler):
    ARGUMENT_PREFIX = '--'
    PARSE_ARGUMENTS = ['root_dir', 'source_list']

    def __init__(self, parser=None):
        self.parser = parser if parser is not None else argparse.ArgumentParser()
        self.source_list_path = None

    def parse_arguements(self):
        for argument in self.PARSE_ARGUMENTS:
            argument = self.ARGUMENT_PREFIX + argument
            self.parser.add_argument(argument, required=True)

        args = vars(self.parser.parse_args())

        root_dir = args[self.PARSE_ARGUMENTS[0]]
        source_list_path = args[self.PARSE_ARGUMENTS[1]]

        self.source_list_path = source_list_path

        return root_dir, source_list_path

    def get_all_sources(self) -> list:
        with open(self.source_list_path, 'r') as file:
            source_list = [line.strip() for line in file]

        return source_list

from datetime import datetime, date


class DateTimeProvider:
    DATE_FORMAT = '%Y-%m-%d'
    DATETIME_FORMAT = '%Y-%m-%dT%H.%M.%S'

    @staticmethod
    def get_current_datetime():
        return datetime.now()

    @staticmethod
    def get_current_date():
        return date.today()

    @classmethod
    def get_current_date_formatted_string(cls):
        current_date = cls.get_current_date()
        current_date_str = current_date.strftime(cls.DATE_FORMAT)
        return current_date_str

    @classmethod
    def datetime_to_str(cls, input_datetime, datetime_format=None):
        if datetime_format is None:
            datetime_format = cls.DATETIME_FORMAT
        return input_datetime.strftime(datetime_format)

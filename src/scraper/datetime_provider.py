from datetime import datetime


class DateTimeProvider:
    @staticmethod
    def get_current_datetime():
        return datetime.now()

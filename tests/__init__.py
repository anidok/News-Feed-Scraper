import datetime


def datetime_converter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

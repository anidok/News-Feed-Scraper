import datetime


# pylint: disable=inconsistent-return-statements
def datetime_converter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()

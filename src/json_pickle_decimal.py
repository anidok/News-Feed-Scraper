import decimal
from typing import Any
from jsonpickle.handlers import BaseHandler
import jsonpickle


class JsonPickleDecimal:
    @staticmethod
    def encode(values: Any):
        jsonpickle.set_preferred_backend('simplejson')
        jsonpickle.set_encoder_options('simplejson', use_decimal=True, sort_keys=True)

        SimpleDecimalHandler.handles(decimal.Decimal)
        return jsonpickle.encode(values, unpicklable=False)

    @staticmethod
    def decode(json: str) -> Any:
        jsonpickle.set_preferred_backend('simplejson')
        jsonpickle.set_decoder_options('simplejson', use_decimal=True)
        return jsonpickle.decode(json)


class SimpleDecimalHandler(BaseHandler):
    """
    This is currently required to work around lack of support for Decimals in Json pickle. The support is meant to have
    been added in version 1.1, and is documented, but at the time of writing, it's missing from the actual shipped code
    Once the library reaches it's next version, this can be re-evaluated and potentially removed in favour of the new
    use_decimal argument to the encode function. More information:
    https://github.com/jsonpickle/jsonpickle/issues/244
    https://stackoverflow.com/questions/54276418/jsonpickle-with-simplejson-backend-serializes-decimal-as-null
    """
    def flatten(self, obj, data):
        return obj

    def restore(self, obj):
        return obj

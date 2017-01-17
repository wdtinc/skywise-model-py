from voluptuous import Any, Schema
from . import ModelApiResource
from ._validation import datetime, datetime_to_str
from ._variable import Variable


class Forecast(ModelApiResource):

    _path = '/models/{model_id}/forecasts'

    _args = Schema({
        'start': datetime_to_str,
        'end': datetime_to_str,
        'initTime': datetime_to_str,
        'limit': int,
        'sort': Any('asc', 'desc'),
        'status': Any(str, unicode)
    })

    _deserialize = Schema({
        'id': Any(str, unicode),
        'model': Any(str, unicode),
        'createTime': datetime,
        'initTime': datetime,
        'variables': Any(str, unicode),
        'status': Any(str, unicode),
        'model_id': Any(str, unicode)
    })

    _serialize = Schema({
        'id': Any(None, str, unicode),
        'model_id': Any(str, unicode),
        'initTime': datetime_to_str,
        'status': Any(str, unicode)
    })

    def get_variables(self, **kwargs):
        return Variable.find(forecast_id=self.id, **kwargs)

    def add_variable(self, platform_forecast):
        variable = Variable()
        variable.forecast_id = self.id
        variable.platform_product_id = platform_forecast.product.id
        variable.platform_forecast_id = platform_forecast.id
        variable.save()
        return variable

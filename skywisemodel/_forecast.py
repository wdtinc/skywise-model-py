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
        'status': unicode
    })

    _deserialize = Schema({
        'id': Any(None, unicode),
        'model': unicode,
        'createTime': datetime,
        'initTime': datetime,
        'variables': unicode,
        'status': unicode,
        'model_id': unicode
    })

    _serialize = Schema({
        'id': Any(None, unicode),
        'model_id': unicode,
        'initTime': datetime_to_str,
        'status': unicode
    })

    def get_variables(self, **kwargs):
        return Variable.find(forecast_id=self.id, **kwargs)

    def add_variable(self, platform_product_id, platform_forecast_id):
        variable = Variable()
        variable.forecast_id = self.id
        variable.platform_forecast_product_id = platform_product_id
        variable.platform_forecast_id = platform_forecast_id
        variable.save()
        return variable

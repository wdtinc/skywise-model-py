from voluptuous import Any, Schema
from . import ModelApiResource
from ._validation import datetime, datetime_to_str
from ._variable import Variable


_forecast_deserialize = Schema({
    'id': Any(None, unicode),
    'model': unicode,
    'createTime': datetime,
    'initTime': datetime,
    'variables': unicode,
    'status': unicode,
    'model_id': unicode
})

_forecast_serialize = Schema({
    'id': Any(None, unicode),
    'model_id': unicode,
    'initTime': datetime_to_str,
    'status': unicode
})


class _ForecastMixin(object):

    def get_variables(self, **kwargs):
        return Variable.find(forecast_id=self.id, **kwargs)

    def add_variable(self, platform_product_id, platform_forecast_id):
        variable = Variable()
        variable.forecast_id = self.id
        variable.platform_forecast_product_id = platform_product_id
        variable.platform_forecast_id = platform_forecast_id
        variable.save()
        return variable


class Forecast(ModelApiResource, _ForecastMixin):

    _path = '/models/{model_id}/forecasts'

    _args = Schema({
        'start': datetime_to_str,
        'end': datetime_to_str,
        'initTime': datetime_to_str,
        'limit': int,
        'sort': Any('asc', 'desc'),
        'status': unicode
    })

    _deserialize = _forecast_deserialize

    _serialize = _forecast_serialize

    @classmethod
    def find(cls, id_=None, **kwargs):
        if id_ is not None:
            return _ForecastById.find(id_)
        return super(Forecast, cls).find(**kwargs)


class _ForecastById(Forecast, _ForecastMixin):

    _path = '/forecasts'

    _deserialize = _forecast_deserialize

    _serialize = _forecast_serialize

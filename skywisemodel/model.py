from voluptuous import Any, Schema

from . import ModelApiResource
from ._forecast import Forecast


class Model(ModelApiResource):

    _path = '/models'

    _deserialize = Schema({
        'id': Any(str, unicode),
        'name': Any(str, unicode),
        'description': Any(str, unicode),
        'forecasts': Any(str, unicode)
    })

    _serialize = Schema({
        'id': Any(None, str, unicode),
        'name': Any(str, unicode),
        'description': Any(str, unicode),
        'forecasts': Any(str, unicode)
    })

    def get_forecasts(self, **kwargs):
        return Forecast.find(model_id=self.id, **kwargs)

    def create_forecast(self, init_time):
        forecast = Forecast()
        forecast.initTime = init_time
        forecast.model_id = self.id
        forecast.save()
        return forecast

    def get_forecast_products(self, **kwargs):
        return _ModelPlatformForecastProduct.find(model_id=self.id, **kwargs)

    def add_forecast_product(self, forecast_product):
        p = _ModelPlatformForecastProduct()
        p.name = forecast_product.name
        p.description = forecast_product.description
        p.platform_product_id = forecast_product.id
        p.model_id = self.id
        p.save()


class _ModelPlatformForecastProduct(ModelApiResource):

    _path = '/models/{model_id}/platform-forecast-products'

    _deserialize = Schema({
        'id': Any(str, unicode),
        'name': Any(str, unicode),
        'description': Any(str, unicode),
        'model_id': Any(str, unicode),
        'platform_forecast_product_id': Any(str, unicode)
    })

    _serialize = Schema({
        'name': Any(str, unicode),
        'description': Any(str, unicode),
        'model_id': Any(str, unicode),
        'platform_forecast_product_id': Any(str, unicode)
    })

    def save(self, **kwargs):
        super(_ModelPlatformForecastProduct, self).save(model_id=self.model_id, **kwargs)

from voluptuous import Any, Schema

from . import ModelApiResource
from ._forecast import Forecast
from ._subscription import Subscription


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

    def get_platform_forecast_products(self, **kwargs):
        return _ModelPlatformForecastProduct.find(model_id=self.id, **kwargs)

    def add_platform_forecast_product(self, name, description, platform_forecast_product_id):
        p = _ModelPlatformForecastProduct()
        p.name = name
        p.description = description
        p.platform_forecast_product_id = platform_forecast_product_id
        p.model_id = self.id
        p.save()

    def subscribe(self, event, subscriber_email):
        subscription = Subscription()
        subscription.model_id = self.id
        subscription.event = event
        subscription.subscriber_email = subscriber_email
        subscription.save()
        return subscription


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

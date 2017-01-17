import arrow
from skywiseplatform import Product
from skywisemodel import Model
from tests import load_fixture
from tests.unit import ModelTest


class EverythingTest(ModelTest):

    def setUp(self):

        super(EverythingTest, self).setUp()

        model = Model()
        model.name = 'tropical-gfe'
        model.description = 'WeatherOps AWIPS II GFE tropical forecast.'

        model_json = load_fixture('model')
        self.model_api_adapter.register_uri('POST', '/models', json=model_json)
        model.save()
        self.model = model

    def test_crud_model(self):

        # Test Create
        model = Model()
        model.name = 'tropical-gfe'
        model.description = 'WeatherOps AWIPS II GFE tropical forecast.'
        model.platform_model_key = 'tropical-gfe'

        model_json = load_fixture('model')
        self.model_api_adapter.register_uri('POST', '/models', json=model_json)
        model.save()

        self.assertEqual(model.id, model_json['id'])
        self.assertEqual(model.name, model_json['name'])
        self.assertEqual(model.description, model_json['description'])

        # Test Update
        model.description = 'Weather Ops Description Changed'
        model_json['description'] = model.description
        self.model_api_adapter.register_uri('PUT', '/models/%s' % model.id, json=model_json)
        model.save()
        self.assertEqual(model.description, 'Weather Ops Description Changed')

        # Test Read
        self.model_api_adapter.register_uri('GET', '/models/%s' % model.id, json=model_json)
        model = Model.find(model_json['id'])
        self.assertEqual(model.id, model_json['id'])

        # Test Delete
        self.model_api_adapter.register_uri('DELETE', '/models/%s' % model.id)
        model.destroy()
        self.assertEqual(model.id, None)

    def test_crud_model_platform_forecast_products(self):

        # Test Create
        self.platform_api_adapter.register_uri('GET', '/products',
                                               json=load_fixture('platform_forecast_products'))
        products = Product.find()
        models_json = []
        for product in products:
            json = {
                'id': 'some-internal-uuid',
                'name': product.name,
                'description': product.description,
                'model_id': self.model.id,
                'platform_forecast_product_id': product.id
            }
            models_json.append(json)
            m = self.model_api_adapter.register_uri('POST', '/models/%s/platform-forecast-products' % json['model_id'],
                                          json=json)
            self.model.add_forecast_product(product)
            self.assertEqual(len(m.request_history), 1)

        # Test Read
        self.model_api_adapter.register_uri('GET', '/models/%s/platform-forecast-products' % self.model.id,
                                  json=models_json)
        forecast_products = self.model.get_forecast_products()
        self.assertEqual(len(forecast_products), 10)

        # Test Update
        model_platform_forecast_product = forecast_products[0]
        original_id = model_platform_forecast_product.id
        model_platform_forecast_product.description = u'My New Description'
        json_response = {
            'id': model_platform_forecast_product.id,
            'description': 'My New Description',
            'model_id': self.model.id,
            'platform_forecast_product_id': model_platform_forecast_product.platform_forecast_product_id
        }
        url = '/models/%s/platform-forecast-products/%s' % (self.model.id, model_platform_forecast_product.id)
        self.model_api_adapter.register_uri('PUT', url, json=json_response)
        model_platform_forecast_product.save()
        self.assertEqual(original_id, model_platform_forecast_product.id)
        self.assertEqual('My New Description', model_platform_forecast_product.description)

        # Test Delete
        url = '/models/%s/platform-forecast-products/%s' % (self.model.id, model_platform_forecast_product.id)
        self.model_api_adapter.register_uri('DELETE', url)
        model_platform_forecast_product.destroy()
        self.assertIsNone(model_platform_forecast_product.id)

    def test_crd_forecast(self):

        forecasts_json = load_fixture('forecasts')

        # Create
        self.model_api_adapter.register_uri('POST', '/models/%s/forecasts' % self.model.id,
                                  json=forecasts_json[0])
        forecast = self.model.create_forecast(arrow.get().datetime)
        self.assertEqual(forecast.id, forecasts_json[0]['id'])

        # Read
        self.model_api_adapter.register_uri('GET', '/models/%s/forecasts' % self.model.id,
                                  json=forecasts_json)
        forecasts = self.model.get_forecasts()
        self.assertEqual(len(forecasts), 2)

        # Delete
        self.model_api_adapter.register_uri('DELETE', '/models/%s/forecasts/%s' % (self.model.id, forecast.id))
        forecast.destroy()
        self.assertIsNone(forecast.id)

    def test_cr_forecast_variable(self):

        # Setup Forecast
        forecasts_json = load_fixture('forecasts')
        self.model_api_adapter.register_uri('POST', '/models/%s/forecasts' % self.model.id,
                                  json=forecasts_json[0])
        forecast = self.model.create_forecast(arrow.get().datetime)

        # Create
        platform_forecast_product_id = "17083b4a-e9fe-11e4-b02c-1681e6b88ec1"
        self.platform_api_adapter.register_uri('GET', '/products/%s' % platform_forecast_product_id,
                                               json=load_fixture('platform_forecast_products').pop(0))
        platform_product = Product.find(platform_forecast_product_id)

        self.platform_api_adapter.register_uri('GET', '/products/%s/forecasts' % platform_forecast_product_id,
                                               json=load_fixture('forecasts'))
        platform_forecast = platform_product.forecasts()[0]

        json = {
            'id': 'my-forecast-variable-id',
            'name': 'a-forecast-variable',
            'description': 'A Forecast Variable.',
            'validTimes': ["2015-05-01T00:00Z", "2015-05-02T00:00Z"],
            'forecast': '/path/to/this-variables/forecast',
            'forecast_id': forecast.id,
            'platform_forecast_product_id': platform_product.id,
            'platform_forecast_id': 'this-platform-forecast-id',
        }
        m = self.model_api_adapter.register_uri('POST', '/forecasts/%s/variables' % forecast.id,
                                      json=json)
        forecasts_json[0]['id'] = 'COMPLETE'
        self.model_api_adapter.register_uri('GET', '/models/%s/forecasts/%s' % (self.model.id,
                                                                       forecasts_json[0]['id']),
                                  json=forecasts_json[0])
        forecast.add_variable(platform_forecast)
        self.assertEqual(len(m.request_history), 1)
        self.assertEqual(forecast.status, 'COMPLETE')

        # Read
        self.model_api_adapter.register_uri('GET', '/forecasts/%s/variables' % forecast.id,
                                  json=[json])
        variables = forecast.get_variables()
        self.assertEqual(len(variables), 1)

        # Test Time Series
        variable = variables[0]
        timeseries_json = load_fixture('timeseries')

        d = {
            "p_id": variable.id,
            "lat": 35.0,
            "lon": 97.0
        }
        self.model_api_adapter.register_uri('GET', '/variables/{p_id}/timeseries/{lat}/{lon}'.format(**d),
                                  json=timeseries_json)
        timeseries = variable.get_timeseries(d["lat"], d["lon"])
        self.assertEqual(len(timeseries.series), 5)
        s = sum([t['value'] for t in timeseries.series])
        self.assertEqual(s, 65.0)
        self.assertEqual(timeseries.mean, 13.0)
        self.assertEqual(timeseries.mode, 15.0)
        self.assertEqual(timeseries.median, 15.0)
        self.assertEqual(timeseries.unit['description'], 'temperature')
        self.assertEqual(timeseries.unit['label'], 'celsius')

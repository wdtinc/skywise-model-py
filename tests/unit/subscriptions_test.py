from skywisemodel import Model
from tests import load_fixture
from tests.unit import ModelTest


class SubscriptionsTest(ModelTest):

    def setUp(self):

        super(SubscriptionsTest, self).setUp()

        model = Model()
        model.name = 'tropical-gfe'
        model.description = 'WeatherOps AWIPS II GFE tropical forecast.'

        model_json = load_fixture('model')
        self.model_api_adapter.register_uri('POST', '/models', json=model_json)
        model.save()
        self.model = model

    def test_subscribe(self):
        subscription_json = load_fixture('subscription')
        event = subscription_json['event']
        subscriber_email = subscription_json['subscriber_email']

        url = '/models/%s/subscriptions' % self.model.id
        self.model_api_adapter.register_uri('POST', url, json=subscription_json)

        subscription = self.model.subscribe(event, subscriber_email)
        self.assertIsNotNone(subscription.id)
        self.assertEqual(subscription.model_id, self.model.id)
        self.assertEqual(subscription.event, event)
        self.assertEqual(subscription.subscriber_email, subscriber_email)
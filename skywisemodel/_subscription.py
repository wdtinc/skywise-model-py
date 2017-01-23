from voluptuous import Any, Schema
from . import ModelApiResource

_subscription_deserialize = Schema({
    'id': Any(None, str, unicode),
    'model_id': Any(str, unicode),
    'event': Any(str, unicode),
    'subscriber_email': Any(str, unicode)
})

_subscription_serialize = Schema({
    'id': Any(None, str, unicode),
    'model_id': Any(str, unicode),
    'event': Any(str, unicode),
    'subscriber_email': Any(str, unicode)
})


class Subscription(ModelApiResource):

    _path = '/models/{model_id}/subscriptions'

    _deserialize = _subscription_deserialize

    _serialize = _subscription_serialize

    @classmethod
    def find(cls, id_=None, **kwargs):
        if id_ is not None:
            return _SubscriptionById.find(id_)
        return super(Subscription, cls).find(**kwargs)


class _SubscriptionById(ModelApiResource):

    _path = '/subscriptions'

    _deserialize = _subscription_deserialize

    _serialize = _subscription_serialize

from voluptuous import Any, Schema
from . import ModelApiResource


class Subscription(ModelApiResource):

    _path = '/models/{model_id}/subscriptions'

    _deserialize = Schema({
        'id': Any(None, str, unicode),
        'model_id': Any(str, unicode),
        'event': Any(str, unicode),
        'subscriber_email': Any(str, unicode)
    })

    _serialize = Schema({
        'id': Any(None, str, unicode),
        'model_id': Any(str, unicode),
        'event': Any(str, unicode),
        'subscriber_email': Any(str, unicode)
    })

    @classmethod
    def find(cls, id_=None, **kwargs):
        if id_ is not None:
            return _SubscriptionById.find(id_)
        return super(Subscription, cls).find(**kwargs)


class _SubscriptionById(Subscription):

    _path = '/subscriptions/{subscription_id}'

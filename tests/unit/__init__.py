import requests_mock
from unittest import TestCase

from skywisemodel import ModelApiResource
from skywiseplatform import PlatformResource


class ModelTest(TestCase):

    def setUp(self):
        ModelApiResource.set_site('http://my.skywise.host')
        ModelApiResource.set_user('my-skywise-user')
        ModelApiResource.set_password('my-skywise-password')
        ModelApiResource.set_use_session_for_async(True)

        self.model_api_adapter = requests_mock.Adapter()
        session = ModelApiResource.get_session()
        session.mount('http://my.skywise.host', self.model_api_adapter)

        PlatformResource.set_site('http://my.skywise.host')
        PlatformResource.set_user('my-skywise-user')
        PlatformResource.set_password('my-skywise-password')
        PlatformResource.set_use_session_for_async(True)

        self.platform_api_adapter = requests_mock.Adapter()
        session = PlatformResource.get_session()
        session.mount('http://my.skywise.host', self.platform_api_adapter)

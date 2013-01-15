from tornado.testing import LogTrapTestCase, AsyncHTTPTestCase

from .base import ApplicationMixin


class BaseHandlerTest(ApplicationMixin, LogTrapTestCase, AsyncHTTPTestCase):
    "Common base class for testing handlers."


class RootHandlerTest(BaseHandlerTest):

    def test_render(self):
        "Render the server root"
        self.http_client.fetch(self.get_url('/'), self.stop)
        response = self.wait()
        self.assertEqual(response.code, 200)


class HostHandlerTest(BaseHandlerTest):

    def get_plugins(self):
        return {'test-host': {'plugins': {'foo': 'bar'}}}

    def test_valid_hostname(self):
        "Render valid host info"
        self.http_client.fetch(self.get_url('/host/test-host'), self.stop)
        response = self.wait()
        self.assertEqual(response.code, 200)
        self.assertTrue('test-host' in response.body)

    def test_invalid_hostname(self):
        "Return a 404 on invalid hostname"
        self.http_client.fetch(self.get_url('/host/invalid-host'), self.stop)
        response = self.wait()
        self.assertEqual(response.code, 404)

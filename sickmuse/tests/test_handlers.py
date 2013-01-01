from tornado.testing import LogTrapTestCase, AsyncHTTPTestCase

from ..app import APIApplication


class RootHandlerTest(LogTrapTestCase, AsyncHTTPTestCase):

    def get_app(self):
        return APIApplication()

    def test_render(self):
        "Render the server root"
        self.http_client.fetch(self.get_url('/'), self.stop)
        response = self.wait()
        self.assertEqual(response.code, 200)


class HostHandlerTest(LogTrapTestCase, AsyncHTTPTestCase):

    def get_app(self):
        application = APIApplication()
        # Fake parsed plugin info
        application.plugin_info = {
            'test-host': {'plugins': {'foo': 'bar'}},
        }
        return application

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

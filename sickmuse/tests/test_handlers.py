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

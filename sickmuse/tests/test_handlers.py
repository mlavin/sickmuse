import json
import os

from tornado.testing import LogTrapTestCase, AsyncHTTPTestCase

from .base import ApplicationMixin, patch


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
        return {'test-host': {'plugins': {'foo': ['bar', ]}}}

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


class MetricHandlerTest(BaseHandlerTest):

    def get_plugins(self):
        return {
            'test-host': {
                'plugins': {
                    'foo': ['bar', ],
                    'xxx': ['yyy', 'zzz', ]
                }
            }
        }

    def test_get_metrics(self):
        """Get metric info for a host/plugin."""
        with patch('sickmuse.handlers.rrdtool') as mock_rrdtool:
            mock_rrdtool.fetch.return_value = [
                # Start, End, Resolution
                (1492183000, 1492186640, 70),
                # Metrics
                ('baz', ),
                # Data
                [(1, ), (2, ), (3, ), ]
            ]
            self.http_client.fetch(self.get_url('/api/test-host/foo'), self.stop)
            response = self.wait()
            file_path = os.path.join(self.rrd_directory, 'test-host', 'foo', 'bar.rrd')
            mock_rrdtool.fetch.assert_called_once_with(
                file_path, 'AVERAGE', '--start', '-1h', '--resolution', '60'
            )
            self.assertEqual(response.code, 200)
            self.assertEqual(response.headers['Content-Type'], 'application/json; charset=UTF-8')
            result = json.loads(response.body)
            expected = {
                'units': None,
                'instances': {
                    'bar': {
                        'start': 1492183000,
                        'end': 1492186640,
                        'resolution': 70,
                        'timeline': [1, 2, 3]
                    }
                }
            }
            self.assertEqual(result, expected)

    def test_plugin_with_mutliple_instances(self):
        """Get more complex plugin info."""
        with patch('sickmuse.handlers.rrdtool') as mock_rrdtool:
            mock_rrdtool.fetch.return_value = [
                # Start, End, Resolution
                (1492183000, 1492186640, 70),
                # Metrics
                ('baz', ),
                # Data
                [(1, ), (2, ), (3, ), ]
            ]
            self.http_client.fetch(self.get_url('/api/test-host/xxx'), self.stop)
            response = self.wait()
            file_path = os.path.join(self.rrd_directory, 'test-host', 'xxx', 'yyy.rrd')
            mock_rrdtool.fetch.assert_any_call(
                file_path, 'AVERAGE', '--start', '-1h', '--resolution', '60'
            )
            file_path = os.path.join(self.rrd_directory, 'test-host', 'xxx', 'zzz.rrd')
            mock_rrdtool.fetch.assert_any_call(
                file_path, 'AVERAGE', '--start', '-1h', '--resolution', '60'
            )
            self.assertEqual(response.code, 200)
            self.assertEqual(response.headers['Content-Type'], 'application/json; charset=UTF-8')
            result = json.loads(response.body)
            expected = {
                'units': None,
                'instances': {
                    'yyy': {
                        'start': 1492183000,
                        'end': 1492186640,
                        'resolution': 70,
                        'timeline': [1, 2, 3]
                    },
                    'zzz': {
                        'start': 1492183000,
                        'end': 1492186640,
                        'resolution': 70,
                        'timeline': [1, 2, 3]
                    }
                }
            }
            self.assertEqual(result, expected)

    def test_plugin_with_multiple_metrics(self):
        """Get more complex metric info."""
        with patch('sickmuse.handlers.rrdtool') as mock_rrdtool:
            mock_rrdtool.fetch.return_value = [
                # Start, End, Resolution
                (1492183000, 1492186640, 70),
                # Metrics
                ('blip', 'blah', ),
                # Data
                [(1, 4, ), (2, 5, ), (3, 6), ]
            ]
            self.http_client.fetch(self.get_url('/api/test-host/foo'), self.stop)
            response = self.wait()
            file_path = os.path.join(self.rrd_directory, 'test-host', 'foo', 'bar.rrd')
            mock_rrdtool.fetch.assert_called_once_with(
                file_path, 'AVERAGE', '--start', '-1h', '--resolution', '60'
            )
            self.assertEqual(response.code, 200)
            self.assertEqual(response.headers['Content-Type'], 'application/json; charset=UTF-8')
            result = json.loads(response.body)
            expected = {
                'units': None,
                'instances': {
                    'bar-blip': {
                        'start': 1492183000,
                        'end': 1492186640,
                        'resolution': 70,
                        'timeline': [1, 2, 3]
                    },
                    'bar-blah': {
                        'start': 1492183000,
                        'end': 1492186640,
                        'resolution': 70,
                        'timeline': [4, 5, 6]
                    }
                }
            }
            self.assertEqual(result, expected)

    def test_get_time_range(self):
        """Optionally change the time range for the metric data."""
        with patch('sickmuse.handlers.rrdtool') as mock_rrdtool:
            mock_rrdtool.fetch.return_value = [
                # Start, End, Resolution
                (1492183000, 1492186640, 70),
                # Metrics
                ('baz', ),
                # Data
                [(1, ), (2, ), (3, ), ]
            ]
            tests = (
                # Parameter, (Start, Resolution)
                ('1hr', ('-1h', '60')),
                ('3hr', ('-3h', '3600')),
                ('6hr', ('-6h', '3600')),
                ('12hr', ('-12h', '3600')),
                ('24hr', ('-1d', '86400')),
                ('1week', ('-1w', '604800')),
                ('1mon', ('-1mon', '2678400')),
                ('3mon', ('-3mon', '2678400')),
                ('6mon', ('-6mon', '2678400')),
                ('1year', ('-1y', '31622400')),
            )
            for param, (start, resolution) in tests:
                url = self.get_url('/api/test-host/foo') + '?range=' + param
                self.http_client.fetch(url, self.stop)
                self.wait()
                file_path = os.path.join(self.rrd_directory, 'test-host', 'foo', 'bar.rrd')
                mock_rrdtool.fetch.assert_called_once_with(
                    file_path, 'AVERAGE', '--start', start, '--resolution', resolution
                )
                mock_rrdtool.fetch.reset_mock()

    def test_invalid_host(self):
        """Try to fetch metrics for an invalid host."""
        with patch('sickmuse.handlers.rrdtool') as mock_rrdtool:
            self.http_client.fetch(self.get_url('/api/missing-host/foo'), self.stop)
            response = self.wait()
            self.assertFalse(mock_rrdtool.fetch.called)
            self.assertEqual(response.code, 404)

    def test_invalid_plugin(self):
        """Try to fetch metrics for an invalid plugin."""
        with patch('sickmuse.handlers.rrdtool') as mock_rrdtool:
            self.http_client.fetch(self.get_url('/api/test-host/missing'), self.stop)
            response = self.wait()
            self.assertFalse(mock_rrdtool.fetch.called)
            self.assertEqual(response.code, 404)

    def test_invalid_range(self):
        """Handle invalid range parameters."""
        with patch('sickmuse.handlers.rrdtool') as mock_rrdtool:
            url = self.get_url('/api/test-host/foo') + '?range=6b'
            self.http_client.fetch(url, self.stop)
            response = self.wait()
            self.assertFalse(mock_rrdtool.fetch.called)
            self.assertEqual(response.code, 400)

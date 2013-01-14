import glob
import os

import rrdtool

from tornado.web import RequestHandler, HTTPError

from sickmuse import __version__


DATE_RANGE_INFO = (
    ('1hr', {'label': 'Past hour', 'start': '-1h', 'resolution': 60}),
    ('3hr', {'label': 'Past 3 hours', 'start': '-3h', 'resolution': 3600}),
    ('6hr', {'label': 'Past 6 hours', 'start': '-6h', 'resolution': 3600}),
    ('12hr', {'label': 'Past 12 hours', 'start': '-12h', 'resolution': 3600}),
    ('24hr', {'label': 'Past 24 hours', 'start': '-1d', 'resolution': 86400}),
    ('1week', {'label': 'Past week', 'start': '-1w', 'resolution': 604800}),
    ('1mon', {'label': 'Past month', 'start': '-1mon', 'resolution': 2678400}),
    ('3mon', {'label': 'Past 3 months', 'start': '-3mon', 'resolution': 2678400}),
    ('6mon', {'label': 'Past 6 months', 'start': '-6mon', 'resolution': 2678400}),
    ('1year', {'label': 'Past year', 'start': '-1y', 'resolution': 31622400}),
)

DATE_RANGE_MAP = dict(DATE_RANGE_INFO)


UNIT_MAP = {
    # Metric name --> Unit
    'memory': 'bytes',
    'partition': 'bytes',
    'pg_db_size': 'bytes',
    'ps_rss': 'bytes',
    'swap': 'bytes',
    'vs_memory': 'bytes',
}


class TemplateHandler(RequestHandler):
    "Add common elements to the template namespace."

    def get_template_namespace(self):
        namespace = super(TemplateHandler, self).get_template_namespace()
        namespace.update({
            'plugin_info': self.application.plugin_info,
            'debug': self.application.settings.get('debug', False),
            'static_url_prefix': self.application.settings.get('static_url_prefix', '/static/'),
            '__version__': __version__,
        })
        return namespace


class RootHandler(TemplateHandler):
    
    def get(self):
        self.render("index.html")


class HostHandler(TemplateHandler):
    
    def get(self, host_name):
        if host_name not in self.application.plugin_info:
            raise HTTPError(404, 'Host not found')
        context = {
            'host_name': host_name,
            'host_info': self.application.plugin_info[host_name],
            'date_range': DATE_RANGE_INFO,
        }
        self.render("host-detail.html", **context)


class MetricAPIHandler(RequestHandler):
    
    def get(self, host, metric):
        if host not in self.application.plugin_info:
            raise HTTPError(404, 'Host not found')
        plugins = self.application.plugin_info[host].get('plugins', {})
        if metric not in plugins:
            raise HTTPError(404, 'Plugin not found')
        instances = plugins[metric]
        cleaned_data = {
            'units': UNIT_MAP.get(metric),
        }
        instance_data = {}
        offset = self.get_argument('range', default='1hr')
        if offset not in DATE_RANGE_MAP:
            raise HTTPError(400, 'Invalid date range')
        date_range = DATE_RANGE_MAP[offset]
        for instance in instances:
            load_file = str(os.path.join(
                self.application.settings['rrd_directory'],
                host, metric, '%s.rrd' % instance
            ))
            start = str(date_range['start'])
            res = str(date_range['resolution'])
            period, metrics, data = rrdtool.fetch(load_file, 'AVERAGE', '--start', start, '--resolution', res)
            start, end, resolution = period
            default = {'start': start, 'end': end, 'resolution': resolution, 'timeline': []}
            if len(metrics) == 1:
                key = instance
                instance_data[key] = default
            else:
                for name in metrics:
                    key = '%s-%s' % (instance, name)
                    instance_data[key] = default
            for item in data:
                for i, name in enumerate(metrics):
                    if len(metrics) == 1:
                        key = instance
                    else:
                        key = '%s-%s' % (instance, name)
                    instance_data[key]['timeline'].append(item[i])
        cleaned_data['instances'] = instance_data
        self.write(cleaned_data)

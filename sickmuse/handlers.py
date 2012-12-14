import glob
import os

import rrdtool

from tornado.web import RequestHandler, HTTPError

class TemplateHandler(RequestHandler):
    "Add common elements to the template namespace."

    def get_template_namespace(self):
        namespace = super(TemplateHandler, self).get_template_namespace()
        namespace.update({
            'plugin_info': self.application.plugin_info,
            'debug': self.application.settings.get('debug', False),
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
        cleaned_data = {}
        for instance in instances:
            load_file = str(os.path.join(
                self.application.settings['rrd_directory'],
                host, metric, '%s.rrd' % instance
            ))
            period, metrics, data = rrdtool.fetch(load_file, 'AVERAGE', '--start', '-60m', '--resolution', '60')
            start, end, resolution = period
            default = {'start': start, 'end': end, 'resolution': resolution, 'timeline': []}
            if len(metrics) == 1:
                key = instance
                cleaned_data[key] = default
            else:
                for name in metrics:
                    key = '%s-%s' % (instance, name)
                    cleaned_data[key] = default
            for item in data:
                for i, name in enumerate(metrics):
                    if len(metrics) == 1:
                        key = instance
                    else:
                        key = '%s-%s' % (instance, name)
                    cleaned_data[key]['timeline'].append(item[i])
        self.write(cleaned_data)

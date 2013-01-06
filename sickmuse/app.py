import glob
import os

from tornado.ioloop import IOLoop
from tornado.options import define, parse_command_line, options
from tornado.web import Application, url

from .handlers import RootHandler, HostHandler, MetricAPIHandler


define("port", default=8282, type=int, help="Server port")
define("debug", default=False, type=bool, help="Run in debug mode")
define("rrd_directory", default="/var/lib/collectd/rrd/", help="RRD file storage location")
define("prefix", default="", help="URL prefix")


class APIApplication(Application):

    def __init__(self, **kwargs):
        prefix = "/{0}/".format(kwargs.get('prefix', "").strip("/")).replace("//", "/")
        handlers = [
            url(r"{0}".format(prefix), RootHandler, name='index'),
            url(r"{0}host/(.*)".format(prefix), HostHandler, name='host-detail'),
            url(r"{0}api/(.*)/(.*)".format(prefix), MetricAPIHandler, name='api-detail'),
        ]
        # Default settings
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            static_url_prefix="{0}static/".format(prefix),
            rrd_directory=options.rrd_directory,
        )
        settings.update(kwargs)
        super(APIApplication, self).__init__(handlers, **settings)
        rrd_directory = os.path.abspath(self.settings['rrd_directory'])
        # From base directory: host/plugin/instance.rrd
        self.plugin_info = {} # Host --> Plugins --> Instances
        for name in glob.glob(u"%s/*/*/*.rrd" % rrd_directory):
            name = name.replace(u"%s/" % rrd_directory, '')
            host, plugin = os.path.split(os.path.dirname(name))
            instance, _ = os.path.splitext(os.path.basename(name))
            info = self.plugin_info.get(host, {})
            plugins = info.get('plugins', {})
            instances = plugins.get(plugin, [])
            instances.append(instance)
            plugins[plugin] = instances
            self.plugin_info[host] = {'plugins': plugins}


def main():
    # Setup and parse options
    parse_command_line()
    # Start application
    application = APIApplication(debug=options.debug, prefix=options.prefix)
    application.listen(options.port, xheaders=True)
    IOLoop.instance().start()


if __name__ == "__main__":
    main()


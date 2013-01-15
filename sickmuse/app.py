import glob
import logging
import os
import signal
import sys
import time

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop, PeriodicCallback
from tornado.process import task_id
from tornado.options import define, parse_command_line, options
from tornado.web import Application, url

from sickmuse.handlers import RootHandler, HostHandler, MetricAPIHandler


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


def shutdown(server, graceful=True):
    """Shut down the application.

    If a graceful stop is requested, waits for all of the IO loop's
    handlers to finish before shutting down the rest of the process.
    We impose a 10 second timeout.

    Based on http://tornadogists.org/3428652/
    """
    ioloop = IOLoop.instance()

    logging.info("Stopping server...")
    # Stop listening for new connections
    server.stop()

    def final_stop():
        ioloop.stop()
        logging.info("Stopped.")
        sys.exit(0)

    def poll_stop(counts={'remaining': None, 'previous': None}):
        remaining = len(ioloop._handlers)
        counts['remaining'], counts['previous'] = remaining, counts['remaining']
        previous = counts['previous']
        # Wait until we only have only one IO handler remaining.  That
        # final handler will be our PeriodicCallback polling task.
        if remaining == 1:
            final_stop()
        if previous is None or remaining != previous:
            logging.info("Waiting on IO %d remaining handlers", remaining)

    if graceful:
        # Callback to check on remaining handlers.
        poller = PeriodicCallback(poll_stop, 250, io_loop=ioloop)
        poller.start()

        # Give up after 10 seconds of waiting.
        ioloop.add_timeout(time.time() + 10, final_stop)
    else:
        final_stop()


def main():
    # Setup and parse options
    parse_command_line()
    # Create application
    application = APIApplication(
        debug=options.debug, prefix=options.prefix, rrd_directory=options.rrd_directory
    )
    # Create server
    server = HTTPServer(application, xheaders=True)
    # Attach signal handlers
    signal.signal(signal.SIGTERM, lambda sig, frame: shutdown(server, True))
    # This will also catch KeyboardInterrupt exception
    signal.signal(signal.SIGINT, lambda sig, frame: shutdown(server, False))
    # Start the server
    server.listen(options.port, "")
    IOLoop.instance().start()


if __name__ == "__main__":
    main()

"Testings mixins and other helper functionality."
import errno
import os
import shutil
import tempfile

from ..app import APIApplication


class ApplicationMixin(object):
    "Helper class for creating an application instance with certain settings/plugins."

    def setUp(self):
        self.rrd_directory = tempfile.mkdtemp()
        super(ApplicationMixin, self).setUp()

    def tearDown(self):
        try:
            # Delete directory
            shutil.rmtree(self.rrd_directory)
        except OSError, e:
            # No such file or directory
            if e.errno != errno.ENOENT:
                raise
        super(ApplicationMixin, self).tearDown()

    def get_app(self):
        "Build an application instance."
        application = APIApplication(**self.get_settings())
        plugins = self.get_plugins()
        if plugins is not None:
            # Fake parsed plugin info
            application.plugin_info = plugins
        return application

    def get_plugins(self):
        "Return plugin_info dictionary to patch on the application."
        return None

    def get_settings(self):
        "Return settings dictionary to pass to the application."
        return {'rrd_directory': self.rrd_directory}

    def create_rrd_file(self, host, plugin, instance):
        "Create an RRD file for given host, plugin and instance."
        plugin_path = os.path.join(self.rrd_directory, host, plugin)
        try:
            os.makedirs(plugin_path)
        except OSError as e:
            if e.errno != errno.EEXIST or not os.path.isdir(plugin_path):
                raise
        file_name = os.path.join(plugin_path, u'{0}.rrd'.format(instance))
        # Not a real RRD file, just an empty file with RRD extension
        with open(file_name, 'w+') as f:
            f.write('')
        return file_name

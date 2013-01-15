"Testings mixins and other helper functionality."

from ..app import APIApplication


class ApplicationMixin(object):
    "Helper class for creating an application instance with certain settings/plugins."

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
        "Return settings dictionary to pass to the application"
        return {}

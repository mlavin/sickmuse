import os
import unittest

from .base import ApplicationMixin


class ApplicationTest(ApplicationMixin, unittest.TestCase):
    "Application setup/configuration tests."

    def test_basic_rrd_discovery(self):
        "Parse plugin_info from RRD directory."
        test_host = 'testhost'
        test_plugin = 'testplugin'
        test_instance = 'testinstance'
        self.create_rrd_file(test_host, test_plugin, test_instance)
        application = self.get_app()
        self.assertTrue(test_host in application.plugin_info)
        plugins = application.plugin_info[test_host]['plugins']
        self.assertTrue(test_plugin in plugins)
        self.assertTrue(test_instance in plugins[test_plugin])

    def test_multiple_hosts_rrd_discovery(self):
        "Parse plugin_info from RRD directory for multiple hosts."
        test_host = 'testhost'
        other_host = 'otherhost'
        test_plugin = 'testplugin'
        test_instance = 'testinstance'
        self.create_rrd_file(test_host, test_plugin, test_instance)
        self.create_rrd_file(other_host, test_plugin, test_instance)
        application = self.get_app()
        self.assertTrue(test_host in application.plugin_info)
        self.assertTrue(other_host in application.plugin_info)

    def test_multiple_plugins_rrd_discovery(self):
        "Parse plugin_info from RRD directory for multiple plugins."
        test_host = 'testhost'
        test_plugin = 'testplugin'
        other_plugin = 'otherplugin'
        test_instance = 'testinstance'
        self.create_rrd_file(test_host, test_plugin, test_instance)
        self.create_rrd_file(test_host, other_plugin, test_instance)
        application = self.get_app()
        self.assertTrue(test_host in application.plugin_info)
        plugins = application.plugin_info[test_host]['plugins']
        self.assertTrue(test_plugin in plugins)
        self.assertTrue(test_instance in plugins[test_plugin])
        self.assertTrue(other_plugin in plugins)
        self.assertTrue(test_instance in plugins[other_plugin])

    def test_multiple_instances_rrd_discovery(self):
        "Parse plugin_info from RRD directory for multiple instances."
        test_host = 'testhost'
        test_plugin = 'testplugin'
        test_instance = 'testinstance'
        other_instance = 'otherinstance'
        self.create_rrd_file(test_host, test_plugin, test_instance)
        self.create_rrd_file(test_host, test_plugin, other_instance)
        application = self.get_app()
        self.assertTrue(test_host in application.plugin_info)
        plugins = application.plugin_info[test_host]['plugins']
        self.assertTrue(test_plugin in plugins)
        self.assertTrue(test_instance in plugins[test_plugin])
        self.assertTrue(other_instance in plugins[test_plugin])

    def test_non_rrd_file(self):
        "Non-RRD files in the directory should be ignored."
        test_host = 'testhost'
        test_plugin = 'testplugin'
        test_instance = 'testinstance'
        other_instance = 'otherinstance'
        self.create_rrd_file(test_host, test_plugin, test_instance)
        other_name = self.create_rrd_file(test_host, test_plugin, other_instance)
        os.rename(other_name, other_name.replace('.rrd', '.txt'))
        application = self.get_app()
        self.assertTrue(test_host in application.plugin_info)
        plugins = application.plugin_info[test_host]['plugins']
        self.assertTrue(test_plugin in plugins)
        self.assertTrue(test_instance in plugins[test_plugin])
        self.assertFalse(other_instance in plugins[test_plugin])

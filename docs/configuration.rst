Configuration Options
=============================================

Below is a full set of configuration options for the Sick Muse server. These options
are configured on the command line via ``sickmuse --<name>=<value>``.


port
---------------------------------------------

Default: ``8282``

The port on which the server runs.


debug
---------------------------------------------

Default: ``False``

Turns the server into debug mode. In this mode the static resouces will use the
non-compressed version and the Python code changes will auto reload. This setting
is used for local development and should not be used in production.


rrd_directory
---------------------------------------------

Default: ``/var/lib/collectd/rrd/``

This is the directory where the server parses the round robin database files. It
expects this directory to have the structure created by Collectd where the sub-directories
are organized ``/<host-name>/<plugin-name>/<instance>.rrd``.


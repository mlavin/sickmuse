Configuration Options
=============================================

Below is a full set of configuration options for the Sick Muse server. These options
are configured on the command line via ``sickmuse --<name>=<value>``.


debug
---------------------------------------------

Default: ``False``

Turns the server into debug mode. In this mode the static resouces will use the
non-compressed version and the Python code changes will auto reload. This setting
is used for local development and should not be used in production.


port
---------------------------------------------

Default: ``8282``

The port on which the server runs.


prefix
---------------------------------------------

Default: ``""`` (Empty String)

The ``prefix`` argument can be used to run the server on under a url prefix. For instance
if you wanted to run the server under ``sickmuse`` you could start the server with::

    sickmuse --prefix=sickmuse

and then proxy the server with Nginx

.. code-block:: guess

    upstream sickmuse {
        server 127.0.0.1:8282;
    }

    server {
        listen 80;
        server_name example.com;

        location /sickmuse/ {
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header Host $http_host;
            proxy_redirect off;
            proxy_buffering on;
            proxy_intercept_errors on;
            proxy_pass http://sickmuse;
        }
    }

You could then see the server running at http://example.com/sickmuse/.


rrd_directory
---------------------------------------------

Default: ``/var/lib/collectd/rrd/``

This is the directory where the server parses the round robin database files. It
expects this directory to have the structure created by Collectd where the sub-directories
are organized ``/<host-name>/<plugin-name>/<instance>.rrd``.


Installation Guide
=============================================

This section will take you through installing and running the Sick Muse server. Before
installing you should make sure you have Python 2.6 or 2.7 installed as well as
`setuptools <http://pypi.python.org/pypi/setuptools>`_ or
`distribute <http://pypi.python.org/pypi/distribute>`_. It is recommended to
use `pip <http://www.pip-installer.org/>`_ and
`virtualenv <http://pypi.python.org/pypi/virtualenv>`_ as well.

The requirement of `python-rrdtool <https://github.com/pbanaszkiewicz/python-rrdtool>`_
needs to be compiled. Your system needs to have the appropriate header files prior to installation.
For Ubuntu based systems you can install the required header files with ``apt-get``::

    sudo apt-get install libcairo2-dev libpango1.0-dev libglib2.0-dev libxml2-dev librrd-dev

For other operating systems you should use available package managers to install the
headers for Python, libcairo2, libpango, libxml2, libglib2 and librrd.


Install
---------------------------------------------

The recommended method for installing Sick Muse is using ``pip`` but you can also use
``easy_install``::

    pip install sickmuse
    # or
    easy_install sickmuse


Running the Server
----------------------------------------

Sick Muse runs on the `Tornado <http://www.tornadoweb.org/>`_ webserver which is a
single-threaded non-blocking server. Once installed you run this server using the ``sickmuse``
command::

    sickmuse
    
This will start the server running on the default port ``8282``. You can change the port
using the ``--port`` option::

    sickmuse --port=8080

See a :doc:`full list of configuration options</configuration>`.

The server does not daemonize itself so it is recommneded that you use one of the
many available daemonization tools such as `Supervisord <http://supervisord.org/>`_,
`Upstart <http://upstart.ubuntu.com/>`_, or `Runit <http://smarden.org/runit/>`_. An
example Supervisor configuration is given below.


Example Supervisor Configuration
----------------------------------------

An example Supervisor configuration is given below. This file would be placed in
``/etc/conf/supervisor/conf.d/sickmuse.conf``.

.. code-block:: guess

    [program:sickmuse]
    process_name=sickmuse
    command=<path to install>/bin/sickmuse
    numprocs=1
    autostart=true
    autorestart=true

``<path to install>`` would be replaced by eiher the system bin if installed globally
or the virtualenv bin directory if installed in a virtual environment. You can find
this path via::

    which sickmuse


Running Behind a Proxy
----------------------------------------

You may want to run Sick Muse behind a proxy such as Nginx or Apache to serve on its
own domain or to enforce authentication. An example Nginx configuration is given to
run this proxy. This file would be placed in both ``/etc/nginx/sites-available/sickmuse.conf``
and ``/etc/nginx/sites-enabled/sickmuse.conf``.

.. code-block:: guess

    upstream sickmuse {
        server 127.0.0.1:8282;
    }

    server {
        listen 80;
        server_name sickmuse.example.com;

        location / {
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header Host $http_host;
            proxy_redirect off;
            proxy_buffering on;
            proxy_intercept_errors on;
            proxy_pass http://sickmuse;
        }
    }


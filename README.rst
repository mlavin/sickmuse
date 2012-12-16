Sick Muse - Collectd Front-end
=============================================

Sick Muse is an open source web application graphing RRD data stored by
`collectd <http://collectd.org/>`_.


Dependencies
----------------------------------------

Requires Python 2.6 or 2.7 and the following Python libraries:

- tornado >= 2.4 (Available under Apache v2)
- python-rrdtool >= 1.4 (Available under LGPL v3)

These dependencies do not ship with the library but will be resolved during the install::

    pip install sickmuse


Running the Server
----------------------------------------

Sick Muse runs on the `Tornado <http://www.tornadoweb.org/>`_ webserver which is a
single-threaded non-blocking server. Once installed you run this server using the ``sickmuse``
command::

    sickmuse
    
This will start the server running on the default port ``8282``. You can change the port
using the ``--port`` option::

    sickmuse --port=8080

The server does not daemonize itself so it is recommneded that you use one of the
many available daemonization tools such as `Supervisord <http://supervisord.org/>`_,
`Upstart <http://upstart.ubuntu.com/>`_, or `Runit <http://smarden.org/runit/>`_.


License
----------------------------------------

sickmuse is released under the BSD License. See the 
`LICENSE <https://github.com/mlavin/sickmuse/blob/master/LICENSE>`_ file for more details.

In addition to the previously listed Python dependencies, this library makes use of
the following projects which are included in the distribution:

- Twitter Bootstrap (Licensed under Apache v2)
- RequireJS (Licensed under BSD/MIT)
- jQuery (Licensed under MIT)
- Font Awesome (Licensed under CC BY 3.0)
- Flot (Licensed under MIT)
- Backbone (Licensed under MIT)
- Underscore (Licensed under MIT)


Contributing
--------------------------------------

This project is still in its early stages and there may be bugs or rapid
changes to the internal APIs. If you think you've found a bug or are interested in 
contributing to this project check out `sickmuse on Github <https://github.com/mlavin/sickmuse>`_.

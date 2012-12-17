Contributing Guide
=============================================

This guide documents ways to contribute to the Sick Muse project as well as the
tools used to make that easier. The project source code and issue tracking is
hosted on `Github <https://github.com/mlavin/sickmuse/issues>`_.


Getting the Source
------------------------------------

You can clone the repository from Github::

    git clone git://github.com/mlavin/sickmuse.git

However this checkout will be read only. If you want to contribute code you should
create a fork and clone your fork. You can then add the main repository as a remote::

    git clone git@github.com:<your-username>/sickmuse.git
    git remote add upstream git://github.com//mlavin/sickmuse.git
    git fetch upstream


Running the Debug Server
------------------------------------

When running the server from inside the repo you can run the server via::

    python -m sickmuse.app

Similarly you can change the port with the ``--port`` option::

    python -m sickmuse.app --port=8000

Another helpful option for running locally is to use the ``--debug`` option::

    python -m sickmuse.app --debug

This will auto-reload the Python modules as they are changed as well as make it
easier to manage CSS and JS changes which is described below.


Installing JS/CSS Libraries
------------------------------------

The production version of Sick Muse ships with minified versions of the CSS and JS
built from and including its static dependencies. To develop locally you will
need the full versions of these libraries.

You may use the built-in Makefile to grab these. Behind the scenes this will
use `bower package manager <http://twitter.github.com/bower/>`_::

    # Install bower via NPM
    npm install bower
    # Install libraries with bower
    make install-static


Building the CSS
------------------------------------

The CSS used by Sick Muse is built using `LESS <http://lesscss.org/>`_. No changes
should be made to the ``sickmuse.css`` directly. Instead changes should be made to the ``extensions.less``
file. After changes are made to ``extensions.less`` you can create the new compressed CSS with the
Node based complier::

    # Install less from the NPM package
    npm install less
    # Build compressed CSS
    make build-css

When the server is running in debug mode it uses the client-side LESS compiler
to make local development easier.


Building the JS
------------------------------------

The JS used by Sick Muse uses `RequireJS <http://requirejs.org/>`_ to manage its dependency
loading and building the bundled version. Similar to the CSS, no changes should be made
directly to the ``sickmuse-built.js``. To build the bundled JS you will need the
``requirejs`` optimizer::

    # Install requirejs from the NPM package
    npm install requirejs
    # Build compressed JS
    make build-js

When the server is running in debug mode it uses the non-compressed version for
easier debugging.

This project using `JSHint <http://jshint.com/>`_ for JS style and detecting
problematic JS patterns::

    # Install jshint from the NPM package
    npm install jshint
    # Build compressed JS
    make lint-js


Building the Documentation
------------------------------------

The docs are written in `ReST <http://docutils.sourceforge.net/rst.html>`_
and built using `Sphinx <http://sphinx.pocoo.org/>`_. As noted above you can use
tox to build the documentation or you can build them on their own via::

    tox -e docs

or::

    make html

from inside the ``docs/`` directory. 


Submitting a Pull Request
------------------------------------

The easiest way to contribute code or documentation changes is through a pull request.
For information on submitting a pull request you can read the Github help page
https://help.github.com/articles/using-pull-requests.

Pull requests are a place for the code to be reviewed before it is merged. This review
will go over the coding style as well as if it solves the problem indended and fits
in the scope of the project. It may be a long discussion or it might just be a simple
thank you.

Not necessarily every request will be merged but you should not take it personally
if you change is not accepted. If you want to increase the chances of your change
being incorporated then here are some tips.

- Address a known issue. Preference is given to a request that fixes a currently open issue.
- Include documentation and tests when appropriate. New features should be tested and documented. Bugfixes should include tests which demostrate the problem.
- Keep it simple. It's difficult to review a large block of code so try to keep the scope of the change small.

You should also feel free to ask for help writing tests or writing documentation
if you aren't sure how to go about it.

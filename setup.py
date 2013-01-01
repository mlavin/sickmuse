import os
import sys

from setuptools import setup, find_packages


def read_file(filename):
    """Read a file into a string"""
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    try:
        return open(filepath).read()
    except IOError:
        return ''


tests_require = []
if sys.version_info < (2, 7):
    tests_require.append("unittest2")


setup(
    name='sickmuse',
    version=__import__('sickmuse').__version__,
    author='Mark Lavin',
    author_email='markdlavin@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/mlavin/sickmuse',
    license='BSD',
    description=u' '.join(__import__('sickmuse').__doc__.splitlines()).strip(),
    install_requires=('tornado>=2.3', 'python-rrdtool>=1.4', ),
    classifiers=(
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ),
    long_description=read_file('README.rst'),
    tests_require=tests_require,
    zip_safe=False,
    entry_points={
      'console_scripts': ('sickmuse = sickmuse.app:main', )
    },
    test_suite='sickmuse.tests',
)

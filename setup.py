try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import sys
import re


if sys.version_info < (2, 6):
    sys.exit("ewmh >= 0.1.3 requires python >= 2.6")

setup(name='ewmh',
      version=re.findall("__version__ = '(.+)'",
                         open('ewmh/__init__.py').read())[0],
      description=(
          'python implementation of Extended Window Manager Hints, based on'
          ' Xlib'
      ),
      long_description=open('README.rst').read(),
      author='parkouss',
      author_email="j.parkouss@gmail.com",
      url='https://github.com/parkouss/pyewmh',
      packages=['ewmh'],
      install_requires=['python-xlib'],
      license='LGPL',
      classifiers=[
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 3',
          'Intended Audience :: Developers',
      ])

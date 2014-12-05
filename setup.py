try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import sys, re

if sys.version > '3':
    install_requires = ['python3-xlib']
else:
    # I can not specify Xlib as a dependency now as there is no
    # release for python2 on PyPi
    install_requires = []
    if sys.version_info < (2, 6):
        sys.exit("ewmh >= 0.1.3 requires python >= 2.6")

setup(name='ewmh',
      version=re.findall("__version__ = '(.+)'", open('ewmh/__init__.py').read())[0],
      description='python implementation of Extended Window Manager Hints, based on Xlib',
      long_description=open('README.rst').read(),
      author='parkouss',
      author_email="j.parkouss@gmail.com",
      url='https://github.com/parkouss/pyewmh',
      packages=['ewmh'],
      install_requires=install_requires,
      license='LGPL',
)

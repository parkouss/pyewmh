try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import sys

if sys.version > '3':
    install_requires = ['python3-xlib']
else:
    # I can not specify Xlib as a dependency now as there is no
    # release for python2 on PyPi
    install_requires = []

setup(name='ewmh',
      version='0.1',
      description='python implementation of Extended Window Manager Hints, based on Xlib',
      long_description=open('README').read(),
      author='parkouss',
      author_email="j.parkouss@gmail.com",
      url='https://github.com/parkouss/pyewmh',
      py_modules=['ewmh'],
      install_requires=install_requires,
      license='LICENSE.txt',
)

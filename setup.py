try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='ewmh',
      version='0.1',
      description='python implementation of Extended Window Manager Hints, based on Xlib',
      long_description=open('README').read(),
      author='parkouss',
      author_email="j.parkouss@gmail.com",
      url='https://github.com/parkouss/pyewmh',
      py_modules=['ewmh'],
      install_requires=['Xlib'],
      license='LICENSE.txt',
)

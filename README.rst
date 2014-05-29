Description
===========

An implementation of EWMH (Extended Window Manager Hints) for python, based on Xlib.
It allows EWMH-compliant window managers (most modern WMs) to be queried and controlled.

Installation
------------

With Python 3, simply:

.. code-block:: shell
  
  pip install ewmh

Unfortunately for Python 2 users, you will have to manually install
the required dependency **Xlib** from https://pypi.python.org/pypi/python-xlib/0.12,
until the xlib developers upload a Python 2 version to PyPi.

Once this is done, just

.. code-block:: shell
  
  python setup.py install

Documentation
-------------

Online documentation is available here: http://ewmh.readthedocs.org/en/latest/.

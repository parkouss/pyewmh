======================
The ewmh python module
======================

.. automodule:: ewmh.ewmh

--------------
EWMH class
--------------

  .. autoclass:: EWMH
    :members:

--------------
Examples
--------------

These examples are tested on gnome.

Exemple to set the active window in fullscreen mode::

  from ewmh import EWMH
  ewmh = EWMH()
  
  # get the active window
  win = ewmh.getActiveWindow()
  
  # list all possible names states:
  # print EWMH.NET_WM_STATES
  
  # set the state on win
  ewmh.setWmState(win, 1, '_NET_WM_STATE_FULLSCREEN')
  
  # flush request
  ewmh.display.flush()

Exemple to move every iceweasel windows on desktop 2::

  from ewmh import EWMH
  ewmh = EWMH()
  
  # get every displayed windows
  wins = ewmh.getClientList()
  
  # get every iceweasel windows, by looking their class name:
  icewins = filter(lambda w: w.get_wm_class()[1] == 'Iceweasel', wins)
  
  # move them to desktop 2 (desktop numbering starts from 0):
  for w in icewins:
    ewmh.setWmDesktop(w, 1)
  
  # flush requests
  ewmh.display.flush()

Example trying to close every windows on desktop 2::

  from ewmh import EWMH
  ewmh = EWMH()
  
  # get every displayed windows on desktop 2:
  wins = filter(lambda w: ewmh.getWmDesktop(w) == 1, ewmh.getClientList())
  
  # trying to close them:
  for w in wins:
    ewmh.setCloseWindow(w)
  
  # flush requests
  ewmh.display.flush()

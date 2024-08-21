"""
This module intends to provide an implementation of Extended Window Manager
Hints, based on the Xlib modules for python.

See the freedesktop.org `specification
<http://standards.freedesktop.org/wm-spec/wm-spec-latest.html>`_ for more
information.
"""
# mypy: disable_error_code = "no-any-return"
from __future__ import annotations

import time

from Xlib import X, display, protocol
from Xlib.xobject import drawable

try:
    from typing import Any

    from _collections_abc import dict_keys
except ImportError:
    pass

class EWMH:
    """
    This class provides the ability to get and set properties defined by the
    EWMH spec.

    Each property can be accessed in two ways. For example, to get the active
    window::

      win = ewmh.getActiveWindow()
      # or: win = ewmh.getProperty('_NET_ACTIVE_WINDOW')

    Similarly, to set the active window::

      ewmh.setActiveWindow(myWindow)
      # or: ewmh.setProperty('_NET_ACTIVE_WINDOW', myWindow)

    When a property is written, don't forget to really send the notification by
    flushing requests::

      ewmh.display.flush()

    :param _display: the display to use. If not given, Xlib.display.Display()
                     is used.
    :param root: the root window to use. If not given,
                     self.display.screen().root is used.
    """

    NET_WM_WINDOW_TYPES = (
        '_NET_WM_WINDOW_TYPE_DESKTOP', '_NET_WM_WINDOW_TYPE_DOCK',
        '_NET_WM_WINDOW_TYPE_TOOLBAR', '_NET_WM_WINDOW_TYPE_MENU',
        '_NET_WM_WINDOW_TYPE_UTILITY', '_NET_WM_WINDOW_TYPE_SPLASH',
        '_NET_WM_WINDOW_TYPE_DIALOG', '_NET_WM_WINDOW_TYPE_DROPDOWN_MENU',
        '_NET_WM_WINDOW_TYPE_POPUP_MENU', '_NET_WM_WINDOW_TYPE_NOTIFICATION',
        '_NET_WM_WINDOW_TYPE_COMBO', '_NET_WM_WINDOW_TYPE_DND',
        '_NET_WM_WINDOW_TYPE_NORMAL')
    """List of strings representing all known window types."""

    NET_WM_ACTIONS = (
        '_NET_WM_ACTION_MOVE', '_NET_WM_ACTION_RESIZE',
        '_NET_WM_ACTION_MINIMIZE', '_NET_WM_ACTION_SHADE',
        '_NET_WM_ACTION_STICK', '_NET_WM_ACTION_MAXIMIZE_HORZ',
        '_NET_WM_ACTION_MAXIMIZE_VERT', '_NET_WM_ACTION_FULLSCREEN',
        '_NET_WM_ACTION_CHANGE_DESKTOP', '_NET_WM_ACTION_CLOSE',
        '_NET_WM_ACTION_ABOVE', '_NET_WM_ACTION_BELOW')
    """List of strings representing all known window actions."""

    NET_WM_STATES = (
        '_NET_WM_STATE_MODAL', '_NET_WM_STATE_STICKY',
        '_NET_WM_STATE_MAXIMIZED_VERT', '_NET_WM_STATE_MAXIMIZED_HORZ',
        '_NET_WM_STATE_SHADED', '_NET_WM_STATE_SKIP_TASKBAR',
        '_NET_WM_STATE_SKIP_PAGER', '_NET_WM_STATE_HIDDEN',
        '_NET_WM_STATE_FULLSCREEN', '_NET_WM_STATE_ABOVE',
        '_NET_WM_STATE_BELOW', '_NET_WM_STATE_DEMANDS_ATTENTION')
    """List of strings representing all known window states."""

    def __init__(self, _display=None, root=None):
        # type: (display.Display | None, drawable.Window | None) -> None
        self.display = _display or display.Display()
        self.root = root or self.display.screen().root  # type: drawable.Window
        self.__getAttrs = {
            '_NET_CLIENT_LIST':           self.getClientList,
            '_NET_CLIENT_LIST_STACKING':  self.getClientListStacking,
            '_NET_NUMBER_OF_DESKTOPS':    self.getNumberOfDesktops,
            '_NET_DESKTOP_GEOMETRY':      self.getDesktopGeometry,
            '_NET_DESKTOP_VIEWPORT':      self.getDesktopViewPort,
            '_NET_CURRENT_DESKTOP':       self.getCurrentDesktop,
            '_NET_ACTIVE_WINDOW':         self.getActiveWindow,
            '_NET_WORKAREA':              self.getWorkArea,
            '_NET_SHOWING_DESKTOP':       self.getShowingDesktop,
            '_NET_WM_NAME':               self.getWmName,
            '_NET_WM_VISIBLE_NAME':       self.getWmVisibleName,
            '_NET_WM_DESKTOP':            self.getWmDesktop,
            '_NET_WM_WINDOW_TYPE':        self.getWmWindowType,
            '_NET_WM_STATE':              self.getWmState,
            '_NET_WM_ALLOWED_ACTIONS':    self.getWmAllowedActions,
            '_NET_WM_PID':                self.getWmPid,
        }
        self.__setAttrs = {
            '_NET_NUMBER_OF_DESKTOPS':  self.setNumberOfDesktops,
            '_NET_DESKTOP_GEOMETRY':    self.setDesktopGeometry,
            '_NET_DESKTOP_VIEWPORT':    self.setDesktopViewport,
            '_NET_CURRENT_DESKTOP':     self.setCurrentDesktop,
            '_NET_ACTIVE_WINDOW':       self.setActiveWindow,
            '_NET_SHOWING_DESKTOP':     self.setShowingDesktop,
            '_NET_CLOSE_WINDOW':        self.setCloseWindow,
            '_NET_MOVERESIZE_WINDOW':   self.setMoveResizeWindow,
            '_NET_WM_NAME':             self.setWmName,
            '_NET_WM_VISIBLE_NAME':     self.setWmVisibleName,
            '_NET_WM_DESKTOP':          self.setWmDesktop,
            '_NET_WM_STATE':            self.setWmState,
        }

    # ------------------------ setters properties ------------------------

    def setNumberOfDesktops(self, nb):
        # type: (int) -> None
        """
        Set the number of desktops (property _NET_NUMBER_OF_DESKTOPS).

        :param nb: the number of desired desktops"""
        self._setProperty('_NET_NUMBER_OF_DESKTOPS', [nb])

    def setDesktopGeometry(self, w, h):
        # type: (int, int) -> None
        """
        Set the desktop geometry (property _NET_DESKTOP_GEOMETRY)

        :param w: desktop width
        :param h: desktop height"""
        self._setProperty('_NET_DESKTOP_GEOMETRY', [w, h])

    def setDesktopViewport(self, w, h):
        # type: (int, int) -> None
        """
        Set the viewport size of the current desktop
        (property _NET_DESKTOP_VIEWPORT)

        :param w: desktop width
        :param h: desktop height"""
        self._setProperty('_NET_DESKTOP_VIEWPORT', [w, h])

    def setCurrentDesktop(self, i):
        # type: (int) -> None
        """
        Set the current desktop (property _NET_CURRENT_DESKTOP).

        :param i: the desired desktop number"""
        self._setProperty('_NET_CURRENT_DESKTOP', [i, X.CurrentTime])

    def setActiveWindow(self, win):
        # type: (drawable.Window) -> None
        """
        Set the given window active (property _NET_ACTIVE_WINDOW)

        :param win: the window object"""
        self._setProperty('_NET_ACTIVE_WINDOW', [1, X.CurrentTime, win.id],
                          win)

    def setShowingDesktop(self, show):
        # type: (int | bool) -> None
        """
        Set/unset the mode Showing desktop (property _NET_SHOWING_DESKTOP)

        :param show: 1 or True to set the desktop mode, else 0 or False"""
        self._setProperty('_NET_SHOWING_DESKTOP', [int(show)])

    def setCloseWindow(self, win):
        # type: (drawable.Window) -> None
        """
        Close the given window (property _NET_CLOSE_WINDOW)

        :param win: the window object"""
        self._setProperty('_NET_CLOSE_WINDOW',
                          [int(time.mktime(time.localtime())), 1], win)

    def setWmName(self, win, name):
        # type: (drawable.Window, str) -> None
        """
        Set the property _NET_WM_NAME

        :param win: the window object
        :param name: desired name"""
        self._setProperty('_NET_WM_NAME', name, win)

    def setWmVisibleName(self, win, name):
        # type: (drawable.Window, str) -> None
        """
        Set the property _NET_WM_VISIBLE_NAME

        :param win: the window object
        :param name: desired visible name"""
        self._setProperty('_NET_WM_VISIBLE_NAME', name, win)

    def setWmDesktop(self, win, i):
        # type: (drawable.Window, int) -> None
        """
        Move the window to the desired desktop by changing the property
        _NET_WM_DESKTOP.

        :param win: the window object
        :param i: desired desktop number
        """
        self._setProperty('_NET_WM_DESKTOP', [i, 1], win)

    def setMoveResizeWindow(self, win, gravity=0, x=None, y=None, w=None,
                            h=None):
        # type: (drawable.Window, int, int | None, int | None, int | None, int | None) -> None
        """
        Set the property _NET_MOVERESIZE_WINDOW to move or resize the given
        window. Flags are automatically calculated if x, y, w or h are defined.

        :param win: the window object
        :param gravity: gravity (one of the Xlib.X.*Gravity constant or 0)
        :param x: int or None
        :param y: int or None
        :param w: int or None
        :param h: int or None
        """
        # indicate source (application)
        gravity_flags = gravity | 0b0000100000000000
        if x is None:
            x = 0
        else:
            gravity_flags = gravity_flags | 0b0000000100000000
        if y is None:
            y = 0
        else:
            gravity_flags = gravity_flags | 0b0000001000000000
        if w is None:
            w = 0
        else:
            gravity_flags = gravity_flags | 0b0000010000000000
        if h is None:
            h = 0
        else:
            gravity_flags = gravity_flags | 0b0000100000000000
        self._setProperty('_NET_MOVERESIZE_WINDOW',
                          [gravity_flags, x, y, w, h], win)

    def setWmState(self, win, action, state, state2=0):
        # type: (drawable.Window, int, int | str, int | str) -> None
        """
        Set/unset one or two state(s) for the given window (property
        _NET_WM_STATE).

        :param win: the window object
        :param action: 0 to remove, 1 to add or 2 to toggle state(s)
        :param state: a state
        :type state: int or str (see :attr:`NET_WM_STATES`)
        :param state2: a state or 0
        :type state2: int or str (see :attr:`NET_WM_STATES`)
        """
        if not isinstance(state, int):
            state = self.display.get_atom(state, True)
        if not isinstance(state2, int):
            state2 = self.display.get_atom(state2, True)
        self._setProperty('_NET_WM_STATE', [action, state, state2, 1], win)

    # ------------------------ getters properties ------------------------

    def getClientList(self):
        # type: () -> list[drawable.Window | None]
        """
        Get the list of windows maintained by the window manager for the
        property _NET_CLIENT_LIST.

        :return: list of Window objects
        """
        return [self._createWindow(w)
                for w in self._getProperty('_NET_CLIENT_LIST')]

    def getClientListStacking(self):
        # type: () -> list[drawable.Window | None]
        """
        Get the list of windows maintained by the window manager for the
        property _NET_CLIENT_LIST_STACKING.

        :return: list of Window objects"""
        return [self._createWindow(w)
                for w in self._getProperty('_NET_CLIENT_LIST_STACKING')]

    def getNumberOfDesktops(self):
        # type: () -> int
        """
        Get the number of desktops (property _NET_NUMBER_OF_DESKTOPS).

        :return: int"""
        return self._getProperty('_NET_NUMBER_OF_DESKTOPS')[0]

    def getDesktopGeometry(self):
        # type: () -> tuple[int, int]
        """
        Get the desktop geometry (property _NET_DESKTOP_GEOMETRY) as an array
        of two integers [width, height].

        :return: [int, int]"""
        return self._getProperty('_NET_DESKTOP_GEOMETRY')

    def getDesktopViewPort(self):
        # type: () -> tuple[int, int]
        """
        Get the current viewports of each desktop as a list of [x, y]
        representing the top left corner (property _NET_DESKTOP_VIEWPORT).

        :return: list of [int, int]
        """
        return self._getProperty('_NET_DESKTOP_VIEWPORT')

    def getCurrentDesktop(self):
        # type: () -> int
        """
        Get the current desktop number (property _NET_CURRENT_DESKTOP)

        :return: int
        """
        return self._getProperty('_NET_CURRENT_DESKTOP')[0]

    def getActiveWindow(self):
        # type: () -> drawable.Window | None
        """
        Get the current active (toplevel) window or None (property
        _NET_ACTIVE_WINDOW)

        :return: Window object or None
        """
        active_window = self._getProperty('_NET_ACTIVE_WINDOW')
        if not active_window:
            return None
        return self._createWindow(active_window[0])

    def getWorkArea(self):
        # type: () -> tuple[int, int, int, int]
        """
        Get the work area for each desktop (property _NET_WORKAREA) as a list
        of [x, y, width, height]

        :return: a list of [int, int, int, int]
        """
        return self._getProperty('_NET_WORKAREA')

    def getShowingDesktop(self):
        # type: () -> int
        """
        Get the value of "showing the desktop" mode of the window manager
        (property _NET_SHOWING_DESKTOP).  1 means the mode is activated, and 0
        means deactivated.

        :return: int
        """
        return self._getProperty('_NET_SHOWING_DESKTOP')[0]

    def getWmName(self, win):
        # type: (drawable.Window) -> str
        """
        Get the property _NET_WM_NAME for the given window as a string.

        :param win: the window object
        :return: str
        """
        return self._getProperty('_NET_WM_NAME', win)

    def getWmVisibleName(self, win):
        # type: (drawable.Window) -> str
        """
        Get the property _NET_WM_VISIBLE_NAME for the given window as a string.

        :param win: the window object
        :return: str
        """
        return self._getProperty('_NET_WM_VISIBLE_NAME', win)

    def getWmDesktop(self, win):
        # type: (drawable.Window) -> int | None
        """
        Get the current desktop number of the given window (property
        _NET_WM_DESKTOP).

        :param win: the window object
        :return: int
        """
        arr = self._getProperty('_NET_WM_DESKTOP', win)
        return arr[0] if arr else None

    def getWmWindowType(self, win, str=False):
        # type: (drawable.Window, bool) -> list[str] | list[int]
        """
        Get the list of window types of the given window (property
        _NET_WM_WINDOW_TYPE).

        :param win: the window object
        :param str: True to get a list of string types instead of int
        :return: list of (int|str)
        """
        types = self._getProperty('_NET_WM_WINDOW_TYPE', win)
        if not str:
            return types
        return [self._getAtomName(t) for t in types]

    def getWmState(self, win, str=False):
        # type: (drawable.Window, bool) -> list[str] | list[int]
        """
        Get the list of states of the given window (property _NET_WM_STATE).

        :param win: the window object
        :param str: True to get a list of string states instead of int
        :return: list of (int|str)
        """
        states = self._getProperty('_NET_WM_STATE', win)
        if not str:
            return states
        return [self._getAtomName(s) for s in states]

    def getWmAllowedActions(self, win, str=False):
        # type: (drawable.Window, bool) -> list[str] | list[int]
        """
        Get the list of allowed actions for the given window (property
        _NET_WM_ALLOWED_ACTIONS).

        :param win: the window object
        :param str: True to get a list of string allowed actions instead of int
        :return: list of (int|str)
        """
        wAllowedActions = self._getProperty('_NET_WM_ALLOWED_ACTIONS', win)
        if not str:
            return wAllowedActions
        return [self._getAtomName(a) for a in wAllowedActions]

    def getWmPid(self, win):
        # type: (drawable.Window) -> int | None
        """
        Get the pid of the application associated to the given window (property
        _NET_WM_PID)

        :param win: the window object
        """
        arr = self._getProperty('_NET_WM_PID', win)
        return arr[0] if arr else None

    # Another good candidate for AnyOf: https://github.com/python/typing/issues/566
    def _getProperty(self, _type, win=None):
        # type: (str, drawable.Window | None) -> Any  # AnyOf[tuple[int, ...] | str]
        if not win:
            win = self.root
        atom = win.get_full_property(self.display.get_atom(_type),
                                     X.AnyPropertyType)
        if atom:
            return atom.value
        return []

    def _setProperty(self, _type, data, win=None, mask=None):
        # type: (str, str | list[int], drawable.Window | None, int | None) -> None
        """
        Send a ClientMessage event to the root window
        """
        if not win:
            win = self.root
        if isinstance(data, str):
            dataSize = 8
        else:
            data = (data+[0]*(5-len(data)))[:5]
            dataSize = 32

        ev = protocol.event.ClientMessage(
            window=win,
            client_type=self.display.get_atom(_type), data=(dataSize, data))

        if not mask:
            mask = (X.SubstructureRedirectMask | X.SubstructureNotifyMask)
        self.root.send_event(ev, event_mask=mask)

    def _getAtomName(self, atom):
        # type: (int) -> str
        try:
            return self.display.get_atom_name(atom)
        except Exception:
            return 'UNKNOWN'

    def _createWindow(self, wId):
        # type: (int | None) -> drawable.Window | None
        if not wId:
            return None
        return self.display.create_resource_object('window', wId)

    # Another good candidate for AnyOf: https://github.com/python/typing/issues/566
    def getReadableProperties(self):
        # type: () -> dict_keys[str, Any]  # dict_keys[str, AnyOf[(() -> list[Window | None]) | (() -> int) | (() -> tuple[int, int]) | (() -> (Window | None)) | (() -> tuple[int, int, int, int]) | ((win: Window) -> str) | ((win: Window) -> (int | None)) | ((win: Window, str: bool = False) -> (list[str] | list[int]))]
        """
        Get all the readable properties' names
        """
        return self.__getAttrs.keys()

    # Another good candidate for AnyOf: https://github.com/python/typing/issues/566
    def getProperty(self, prop, *args, **kwargs):
        # type: (str, drawable.Window | bool, drawable.Window | bool) -> Any  # AnyOf[int, str, list[Window | None], list[str], list[int], tuple[int, int], tuple[int, int, int, int], Window, None]
        """
        Get the value of a property. See the corresponding method for the
        required arguments.  For example, for the property _NET_WM_STATE, look
        for :meth:`getWmState`
        """
        f = self.__getAttrs.get(prop)
        if not f:
            raise KeyError('Unknown readable property: %s' % prop)
        return f(self, *args, **kwargs)  # type: ignore[operator]  # pyright: ignore[reportGeneralTypeIssues]

    # Another good candidate for AnyOf: https://github.com/python/typing/issues/566
    def getWritableProperties(self):
        # type: () -> dict_keys[str, Any]  # dict_keys[str, AnyOf[((nb: int) -> None) | ((w: int, h: int) -> None) | ((i: int) -> None) | ((win: Window) -> None) | ((show: int | bool) -> None) | ((win: Window, gravity: int = 0, x: int | None = None, y: int | None = None, w: int | None = None, h: int | None = None) -> None) | ((win: Window, name: str) -> None) | ((win: Window, i: int) -> None) | ((win: Window, action: int, state: int | str, state2: int | str = 0) -> None)]
        """Get all the writable properties names"""
        return self.__setAttrs.keys()

    def setProperty(self, prop, *args, **kwargs):
        # type: (str, drawable.Window | str | int | bool | None, drawable.Window | str | int | bool | None) -> None
        """
        Set the value of a property by sending an event on the root window.
        See the corresponding method for the required arguments. For example,
        for the property _NET_WM_STATE, look for :meth:`setWmState`
        """
        f = self.__setAttrs.get(prop)
        if not f:
            raise KeyError('Unknown writable property: %s' % prop)
        f(self, *args, **kwargs)  # type: ignore[operator]  # pyright: ignore[reportGeneralTypeIssues]

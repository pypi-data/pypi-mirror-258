Python GDBus Util
=================

[![Read the Docs](https://readthedocs.org/projects/python-gdbus-util/badge/?version=latest)](https://python-gdbus-util.readthedocs.io/en/latest/)
[![PyPI - Version](https://img.shields.io/pypi/v/gdbus_util.svg)](https://pypi.org/project/gdbus_util/)

A collection of utilities to create GDBus services in Python.


DBusObject
----------

This class can be used to define a D-Bus object and register it on a
D-Bus connection.

See the [`DBusObject` documentation](https://python-gdbus-util.readthedocs.io/en/latest/api/dbus_object.html) 
for more information.

ExitOnIdleService
-----------------
This class implements race-free exit-on-idle for a D-Bus service. It is
useful for services that are meant to be started on demand and exit
automatically when they are no longer needed.

See the [`ExitOnIdleService` documentation](https://python-gdbus-util.readthedocs.io/en/latest/api/exit_on_idle_service.html)
for more information.

Installation
------------

To install the latest release from PyPI:

```bash
pip install gdbus-util
```

Credits
-------
The race-free exit-on-idle implementation was inspired by 
https://github.com/cgwalters/test-exit-on-idle and systemd's 
[`bus_event_loop_with_idle`](https://github.com/systemd/systemd/blob/190ff0d0a8d1fc367ec04296f24cd1cab5b7543b/src/shared/bus-util.c#L97).

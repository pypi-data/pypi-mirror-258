Python GDBus Util
===========

A collection of utilities to create GDBus services in Python.


DBusObject
----------

This is a class that can be used to define a D-Bus object and register
it on a D-Bus service.

Take a look at `examples/simple/hello-service.py` for a simple example
of how to use it.


ExitOnIdleService
-----------------

This class implements race-free exit-on-idle for a D-Bus service. It
is useful for services that are meant to be started on demand and exit
automatically when they are no longer needed.

It takes a timeout in seconds as a parameter and will exit the service
if it is idle at the end of the timeout. A 
[`check_idle`](https://github.com/adombeck/pygdbus-service/blob/main/src/gdbus_util/exit_on_idle.py#L35-L35) 
method can be overridden to implement the idle check. The `DBusObject` 
has a [`check_idle`](https://github.com/adombeck/pygdbus-service/blob/main/src/gdbus_util/dbus_object.py#L140-L143) method which checks if there are any ongoing method 
calls.
If the `ExitOnIdleService` instance is also a `DBusObject`, it will 
use that method as the idle check by default.

The timer can be reset by calling the `reset_idle_timer` method. If the 
`ExitOnIdleService` instance is also a `DBusObject`, it will 
automatically reset the idle timeout whenever a method call is received 
(or a property is read or written).

To avoid that requests are lost when the service is exiting, it
unregisters the bus name first and then handles any pending requests
before exiting.

If the service is run as a systemd service, systemd will
be notified that the service is stopping, so that it will queue any
start requests instead of assuming that the service is still running.

Take a look at `examples/exit-on-idle/hello-service.py` for a simple
example or `examples/more-complex/accounts-service.py` for a more
complex example of how to implement an exit-on-idle service.


Credits
-------
The race-free exit-on-idle implementation was inspired by 
https://github.com/cgwalters/test-exit-on-idle and systemd's 
[`bus_event_loop_with_idle`](https://github.com/systemd/systemd/blob/190ff0d0a8d1fc367ec04296f24cd1cab5b7543b/src/shared/bus-util.c#L97).

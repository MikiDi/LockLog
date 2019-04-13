from datetime import datetime
import logging
import os.path
import sys

from pydbus import SessionBus
from gi.repository import GLib

from .locklog import create_event_handler

def main():
    LOG_FOLDER = sys.argv[1]
    try:
        DBUS_INTERFACE = sys.argv[2]
    except IndexError:
        DBUS_INTERFACE = 'org.gnome.ScreenSaver'
    STARTUP_TIME = datetime.now()
    logging.getLogger().setLevel(logging.INFO)

    loop = GLib.MainLoop()
    bus = SessionBus()
    try:
        dev = bus.get(DBUS_INTERFACE)
    except ValueError:
        logging.error("Failed opening D-Bus interface '{}'\nexiting ...".format(DBUS_INTERFACE))
        sys.exit(1)

    handler = create_event_handler(LOG_FOLDER, STARTUP_TIME)

    try:
        with dev.ActiveChanged.connect(handler) as bus_ses:
            logging.info("Succesfully registered handler for D-Bus event '{}' "
                         "on interface '{}'".format('ActiveChanged',
                                                    DBUS_INTERFACE))
            loop.run()
    except AttributeError as e:
        logging.error("Failed registering handler for D-Bus event '{}' "
                      "on interface '{}' ({})\nexiting ...".format('ActiveChanged',
                                                                   DBUS_INTERFACE,
                                                                   e))
        sys.exit(1)

if __name__ == "__main__":
    main()

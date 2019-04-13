# LockLog

Easily log screen lock- and unlock-events, hereby keeping track of your on-screen time. Useful for productivity tracking.  
The idea was to create something in the fashion of [lastwake.py](https://github.com/arigit/lastwake.py), however, screen lock- and unlock-events aren't logged by default and thus can't be derived from existing log journals.  
This library sets up a D-Bus event-listener for these events and writes them to a daily logfile.

Example `productivity_2019-04-13.log`:
```
  Unlock Timestamp   |   Lock Timestamp    | Active Time |
 ------------------- | ------------------- | ----------- |
 2019-04-13 18:48:18 | 2019-04-13 18:52:31 |    0h  4m   |
 2019-04-13 20:21:26 | 2019-04-13 20:26:41 |    0h  5m   |
 2019-04-13 20:26:53 | 2019-04-13 20:33:22 |    0h  6m   |
 2019-04-13 21:34:03 | 2019-04-13 22:09:22 |    0h 35m   |
 ```

## Installation

`pip3 install git+https://github.com/MikiDi/LockLog#egg=locklog`


## Usage

`locklog /path/to/logfolder`

You can optionally define the D-Bus-interface name of your screensaver (defaults to `org.gnome.ScreenSaver`):

`locklog /path/to/logfolder org.gnome.ScreenSaver`

### Determining the D-Bus-interface name of your screensaver

```
dbus-send \
        --session \
        --dest=org.freedesktop.D-Bus \
        --type=method_call \
        --print-reply \
        /org/freedesktop/D-Bus org.freedesktop.D-Bus.ListNames \
    | grep -io '[^"]*.screensaver'
```
source: https://superuser.com/a/898994, adapted to make regex case insensitive

### Registering as a systemd-service for launch on startup

Create the file `~/.config/systemd/user/locklog.service` and change the log-folder path behind `ExecStart=`.
```
[Unit]
Description=LockLog service
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=1
ExecStart=/usr/bin/env locklog /path/to/logfolder

[Install]
WantedBy=graphical.target
```

Starting the service (starting it right now):  
`systemctl --user start locklog`

enabling the service (start on each boot):  
`systemctl --user enable locklog`

## Credits

- Logging format based on [lastwake.py](https://github.com/arigit/lastwake.py)
- Makes use of the [pydbus](https://github.com/LEW21/pydbus) library
- Learned about D-Bus monitoring here: [Logging lock-screen events](https://superuser.com/questions/662974)
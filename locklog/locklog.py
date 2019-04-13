#!/usr/bin/env python3
import os.path
from datetime import datetime

def create_filename(date):
    return 'productivity_' + date.strftime("%Y-%m-%d") + '.log'

# format-string logic in below function from 'lastwake.py'
# https://github.com/arigit/lastwake.py/blob/fb44bbc0f1433218c3fa22cca3debaacfaa3bf88/lastwake.py#L161
def create_file_heading(date):
    headers = ["Unlock Timestamp", "Lock Timestamp", "Active Time"]
    row_format = " {:^19} |" * 2 + " {:^11} |"
    retval = row_format.format(*headers) + "\n"
    rowSeparator = ("-" * 19, "-" * 19, "-" * 11)
    retval += row_format.format(*rowSeparator) + "\n"
    return retval

# format-string logic in below function from 'lastwake.py'
# https://github.com/arigit/lastwake.py/blob/fb44bbc0f1433218c3fa22cca3debaacfaa3bf88/lastwake.py#L183
def create_row(unlock_time, lock_time):
    timedelta = lock_time - unlock_time
    row_format = " {:^19} |" * 2 + " {:^11} |"
    timeDiff_format = "{:3d}h {:2d}m"
    defaultFormat = "%Y-%m-%d %H:%M:%S"
    row = [
        unlock_time.strftime(defaultFormat),
        lock_time.strftime(defaultFormat),
        timeDiff_format.format(timedelta.seconds//(60 * 60), (timedelta.seconds%(60 * 60))//60)
    ]
    return row_format.format(*row) + '\n'

def create_event_handler(log_folder_path, init_unlock_time):
    unlock_time, lock_time = init_unlock_time, None
    def event_handler(b):
        nonlocal unlock_time, lock_time
        if b: # Screen locked
            lock_time = datetime.now()
            with open(os.path.join(log_folder_path, create_filename(unlock_time)), "a") as f:
                if f.tell() < 2: # HACK: determine if file is newly created
                    f.write(create_file_heading(unlock_time))
                f.write(create_row(unlock_time, lock_time))
        else: # Screen unlocked
            unlock_time = datetime.now()
    return event_handler


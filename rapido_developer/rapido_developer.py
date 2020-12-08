
import os
import bpy  

import threading
import time
from datetime import datetime as dt

from .server import WatchDog

VERSION = bpy.app.version
OS_HASH = {
    'linux': "%s/.config/blender/%d.%d/" % (os.environ.get('HOME', ''), VERSION[0], VERSION[1]),
    'macos': "/Users/%s/Library/Application Support/Blender/%d.%d/" % (os.environ.get('USER', ''), VERSION[0], VERSION[1]),
    'nt': "%s/AppData/Roaming/Blender Foundation/Blender/%d.%d/" % (os.environ.get('USERPROFILE', ''), VERSION[0], VERSION[1]),
}

def get_os():
    for k, v in OS_HASH.items():
        if os.path.exists(v): return k
    return 'unknown'

def get_script_folder():
    script_directory = bpy.context.preferences.filepaths.script_directory
    os = get_os()
    if os == 'unknown':
        return './%d.%d/' % (VERSION[0], VERSION[1])
    else:
        return script_directory if script_directory != '' else '%s/scripts' & OS_HASH[os]

SRVR = None
THREADS = []
STARTUP_TIMESTAMP = dt.now().timestamp()
IS_SCANNING = True

def start_server():
    global SRVR
    SRVR = WatchDog.get_server(get_os(), get_script_folder)
    
    try:
        SRVR.serve_forever()
    except:
        pass

def has_been_quit_recently():

    quit_file = f'{bpy.context.preferences.filepaths.temporary_directory}/quit.blend'

    if os.path.exists(quit_file):
        if os.path.getmtime(quit_file) > STARTUP_TIMESTAMP:
            return True

    return False

def start_alive_scanner():

    global IS_SCANNING

    while IS_SCANNING:
        time.sleep(5)
        if has_been_quit_recently():
            if SRVR: shutdown_server()
            IS_SCANNING = False
    

def shutdown_server():

    global SRVR
    if SRVR: SRVR.shutdown()

    global THREADS
    for t in THREADS: t.join()

    THREADS = []
    SRVR = None

def register():
    global THREADS
    THREADS.append(threading.Thread(target=start_server))
    THREADS.append(threading.Thread(target=start_alive_scanner))
    for t in THREADS: t.start()

def unregister():
    global IS_SCANNING
    IS_SCANNING = False
    shutdown_server()

import os
import sys
import psutil


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except (Exception, SyntaxError):
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


TEMP_FOLDER = resource_path("temp")
RESOURCE_FILE = os.path.join('mail.txt')
CHECK_FILE = resource_path("check.txt")
ERROR_MARK = '[]'
resources = []
drivers = []
checked = {}
PROXY_TYPE = 'http'
VERSION_FILE = os.path.join(TEMP_FOLDER, 'version.txt')
idle = False
exe_name = None
stand_by = False
CWD = resource_path("")
osname = None
schedule_check = None
CHECK = 10
PATCHED_DRIVERS_FOLDER = os.path.join(TEMP_FOLDER, 'patched_drivers')


def load_init_values():
    global osname, exe_name
    from common.file import FileHelper
    osname, exe_name = FileHelper.download_driver()
    if osname == 'win':
        FileHelper.clear_window_app_data()


def init():
    load_init_values()


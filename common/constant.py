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
ERROR_MARK = '[]'
resources = []
driver = []
checked = {}
PROXY_TYPE = 'http'
VERSION_FILE = os.path.join(TEMP_FOLDER, 'version.txt')
idle = False
exe_name = None
stand_by = False
CWD = resource_path("")
osname = None
THREAD_AMOUNT = 2
PATCHED_DRIVERS_FOLDER = os.path.join(TEMP_FOLDER, 'patched_drivers')


def load_init_values():
    global cpu_usage, osname, exe_name, constructor
    cpu_usage = str(psutil.cpu_percent(1))
    from common.file import FileHelper
    osname, exe_name = FileHelper.download_driver()
    if osname == 'win':
        FileHelper.clear_window_app_data()
        import wmi
        constructor = wmi.WMI()


def init():
    load_init_values()


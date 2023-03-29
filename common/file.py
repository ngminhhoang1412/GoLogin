import common.constant as Constant
import platform
import shutil
import subprocess
import sys
import os
import undetected_chromedriver._compat as uc


class FileHelper:

    CHROME = ['{8A69D345-D564-463c-AFF1-A69D9E530F96}',
              '{8237E44A-0054-442C-B6B6-EA0509993955}',
              '{401C381F-E0DE-4B85-8BD8-3F3F14FBDA57}',
              '{4ea16ac7-fd5a-47c3-875b-dbf4a2008c20}']

    def __init__(self):
        pass

    @staticmethod
    def clear_window_app_data():
        user = os.path.expanduser("~")
        tmp_folder = os.path.join(user, "AppData", "Roaming", "undetected_chromedriver")
        shutil.rmtree(tmp_folder, ignore_errors=True)

    @staticmethod
    def is_disk_space_available(percentage):
        total, used, free = shutil.disk_usage("/")
        used_percentage = float(used / total * 100)
        return used_percentage < percentage

    @staticmethod
    def copy_drivers():
        current = os.path.join(Constant.CWD, f'chromedriver{Constant.exe_name}')
        os.makedirs(Constant.PATCHED_DRIVERS_FOLDER, exist_ok=True)
        for i in range(Constant.THREAD_AMOUNT + 1):
            try:
                destination = os.path.join(
                    Constant.PATCHED_DRIVERS_FOLDER, f'chromedriver_{i}{Constant.exe_name}')
                shutil.copy(current, destination)
            except (Exception, SyntaxError):
                pass

    @staticmethod
    def download_driver(patched_drivers=Constant.PATCHED_DRIVERS_FOLDER):
        osname = platform.system()

        if osname == 'Linux':
            osname = 'lin'
            exe_name = ""
            with subprocess.Popen(['google-chrome', '--version'], stdout=subprocess.PIPE) as proc:
                version = proc.stdout.read().decode('utf-8').replace('Google Chrome', '').strip()
        elif osname == 'Darwin':
            osname = 'mac'
            exe_name = ""
            process = subprocess.Popen(
                ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '--version'], stdout=subprocess.PIPE)
            version = process.communicate()[0].decode(
                'UTF-8').replace('Google Chrome', '').strip()
        elif osname == 'Windows':
            osname = 'win'
            exe_name = ".exe"
            version = None
            try:
                process = subprocess.Popen(
                    ['reg', 'query', 'HKEY_CURRENT_USER\\Software\\Google\\Chrome\\BLBeacon', '/v', 'version'],
                    stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL
                )
                version = process.communicate()[0].decode(
                    'UTF-8').strip().split()[-1]
            except (SyntaxError, Exception):
                for i in FileHelper.CHROME:
                    for j in ['opv', 'pv']:
                        try:
                            command = [
                                'reg', 'query', f'HKEY_LOCAL_MACHINE\\Software\\Google\\Update\\Clients\\{i}', '/v',
                                f'{j}', '/reg:32']
                            process = subprocess.Popen(
                                command,
                                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL
                            )
                            version = process.communicate()[0].decode(
                                'UTF-8').strip().split()[-1]
                        except (SyntaxError, Exception):
                            pass

        else:
            input('{} OS is not supported.'.format(osname))
            sys.exit()

        try:
            with open(Constant.VERSION_FILE, 'r') as f:
                previous_version = f.read()
        except (SyntaxError, Exception):
            previous_version = '0'

        with open(Constant.VERSION_FILE, 'w') as f:
            f.write(version)

        if version != previous_version:
            try:
                os.remove(f'chromedriver{exe_name}')
            except (SyntaxError, Exception):
                pass

            shutil.rmtree(patched_drivers, ignore_errors=True)

        major_version = version.split('.')[0]

        uc.TARGET_VERSION = major_version
        uc.install()

        return osname, exe_name

    @staticmethod
    def mark_email(email):
        with open(Constant.RESOURCE_FILE, 'r') as file:
            newline = []
            for line in file.readlines():
                if email in line:
                    newline.append(f"{Constant.ERROR_MARK}{line}")
                else:
                    newline.append(line)
        with open(Constant.RESOURCE_FILE, 'w') as file:
            file.writelines(newline)



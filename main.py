import os
import subprocess
import sys
from random import shuffle
from concurrent.futures import ThreadPoolExecutor
from threading import Timer
import common.constant as Constant
from flow import Flow


def handle_flow(position):
    flow = Flow(position)
    flow.start_flow()


def pause():
    for driver in Constant.drivers:
        driver.quit()
    Constant.drivers = []
    if Constant.schedule_check:
        Constant.schedule_check.cancel()
    subprocess.Popen(f"taskkill /F /T /PID {os.getpid()}", shell=True)


def check():
    with open(Constant.CHECK_FILE, encoding="utf-8") as f:
        first_line = f.readline()
    if first_line != 'true':
        pause()


def get_resource():
    resources = []
    path = Constant.RESOURCE_FILE
    if not os.path.isfile(path):
        raise ValueError('Resource file is required')
    with open(path, encoding="utf-8") as f:
        loaded = [x.strip() for x in f if x.strip() != '']

    for lines in loaded:
        if Constant.ERROR_MARK not in lines:
            split = lines.split(':')
            username = split[0]
            password = split[1]
            backup = split[2]
            p = f"{split[5]}:{split[6]}@{split[3]}:{split[4]}"
            resources.append({
                "proxy": p,
                "email": [
                    username,
                    password,
                    backup
                ]
            })

    resources = list(filter(None, resources))
    shuffle(resources)
    return resources


def schedule_check():
    timer = Timer(Constant.CHECK, schedule_check)
    timer.start()
    Constant.schedule_check = timer
    check()


def main():
    Constant.resources = get_resource()
    pool_number = list(range(len(Constant.resources)))
    if len(Constant.resources) == 0:
        pause()

    with ThreadPoolExecutor(max_workers=len(Constant.resources)) as executor:
        [executor.submit(handle_flow, position) for position in pool_number]


if __name__ == '__main__':
    Constant.init()
    schedule_check()
    while True:
        try:
            main()
        except Exception as e:
            print(e)
            sys.exit()

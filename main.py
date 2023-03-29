import os
import sys
from random import shuffle
from concurrent.futures import ThreadPoolExecutor, wait
import common.constant as Constant
from common.file import FileHelper
from flow import Flow


def handle_flow(position):
    flow = Flow(position)
    flow.start_flow()


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


def main():
    Constant.resources = get_resource()
    pool_number = list(range(len(Constant.resources)))

    with ThreadPoolExecutor(max_workers=Constant.THREAD_AMOUNT) as executor:
        futures = [executor.submit(handle_flow, position) for position in pool_number]
        wait(futures)


if __name__ == '__main__':
    Constant.init()

    while True:
        try:
            print(Constant.RESOURCE_FILE)
            FileHelper.copy_drivers()
            main()
        except KeyboardInterrupt:
            # login gmail ignore this
            sys.exit()

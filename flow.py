import time

import common.constant as Constant
import os
import io
import threading
from undetected_chromedriver.patcher import Patcher
from fake_headers import Headers
from requests.exceptions import RequestException
from requests.exceptions import ProxyError
from login_gmail_selenium.util.profile import ChromeProfile
from common.file import FileHelper


class Flow:
    def __init__(self, position):
        self.driver = None
        self.position = position
        self.gmail = None
        self.proxy = None
        self.proxy_type = None
        self.get_resource()
        self.callback = None
        # Init proxy target

    def setup_proxy(self):
        header = Headers(
            browser="chrome",
            os=Constant.osname,
            headers=False
        ).generate()
        agent = header['User-Agent']

        use_proxy = True
        self.setup_chrome_profile(use_proxy)

    def setup_chrome_profile(self, use_proxy=True):
        patched_driver = os.path.join(
            Constant.PATCHED_DRIVERS_FOLDER, f'chromedriver_{self.position}{Constant.exe_name}')
        try:
            Patcher(executable_path=patched_driver).patch_exe()
        except (Exception, SyntaxError):
            pass

        if use_proxy:
            profile = ChromeProfile(email=self.gmail[0],
                                    password=self.gmail[1],
                                    backup_email=self.gmail[2],
                                    auth_type='private' if '@' in self.proxy else 'public',
                                    path=patched_driver,
                                    prox=self.proxy,
                                    prox_type=self.proxy_type)
        else:
            profile = ChromeProfile(email=self.gmail[0],
                                    password=self.gmail[1],
                                    backup_email=self.gmail[2],
                                    path=patched_driver)
        driver = profile.retrieve_driver()
        Constant.drivers.append(driver)
        self.driver = driver
        profile.start()
        time.sleep(1000000)

    def start_flow(self):
        try:
            try:
                self.setup_proxy()
                # if self.callback:
                #     self.callback()
                self.driver.quit()
            except RequestException as request_err:
                Constant.checked[self.position] = self.proxy_type
                raise request_err
            except ProxyError as proxy_err:
                raise proxy_err
        except Exception as e:
            self.driver.quit()
            raise e

    def get_resource(self):
        position = self.position
        resource = Constant.resources[position]
        current_proxy = resource["proxy"]
        gmail = resource["email"]
        self.gmail = gmail
        proxy = current_proxy

        if Constant.PROXY_TYPE:
            proxy_type = Constant.PROXY_TYPE
        elif '|' in current_proxy:
            split = current_proxy.split('|')
            proxy_type = split[-1]
            proxy = split[0]
        else:
            proxy_type = 'http'
            if Constant.checked[position] == 'http':
                proxy_type = 'socks4'
            if Constant.checked[position] == 'socks4':
                proxy_type = 'socks5'

        self.proxy = proxy
        self.proxy_type = proxy_type
        # TODO: check randomness of proxy here
        # with open("test.txt", "a") as file:
        #     file.write(f"{proxy}\n")

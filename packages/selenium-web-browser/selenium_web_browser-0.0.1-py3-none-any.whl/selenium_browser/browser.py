import os
import logging
from typing import Union
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager as DriverManager


# web driver manager loglama kapat
logging.getLogger('WDM').setLevel(logging.NOTSET)
os.environ['WDM_LOG'] = "0"
os.environ['WDM_LOG_LEVEL'] = "0"


class Browser:

    driver: Union[None, WebDriver] = None
    logger = None

    # driver options
    options = None

    def __new__(cls):

        # logger object is created
        if not cls.logger:
            cls.logger = logging.getLogger("selenium_browser")

        if not cls.options:
            cls.options = Options()

        return super().__new__(cls)

    def __init__(self) -> None:
        self.excludeSwitches = []

    def disable_logging(self):
        self.excludeSwitches.append('enable-logging')

        return self

    def headless(self):
        self.options.add_argument("--headless")

        return self

    def set_user_agent(self, user_agent=None):
        if not user_agent:
            user_agent = os.getenv("USER_AGENT")

        self.options.add_argument(f"user-agent=User-Agent: {user_agent}")

        return self

    def set_profile(self, user_data_dir=None, profile_dir="Default"):
        if not user_data_dir:
            user_data_dir = os.getenv("USER_DATA_DIR")

        self.options.add_argument(f"--user-data-dir={user_data_dir}")
        self.options.add_argument(f"--profile-directory={profile_dir}")

        return self

    def block_popup_windows(self):
        self.excludeSwitches.append('disable-popup-blocking')

        return self

    def set_download_directory(self, dir=None):
        if not dir:
            dir = os.getenv("DOWNLOAD_DIR")

        self.options.add_experimental_option(
            "prefs", {"download.default_directory": dir})

        return self

    def set_window_size(self, width=1920, height=1080):
        self.options.add_argument(f"--window-size={width},{height}")

        return self

    def increase_performance(self):
        # The /dev/shm partition is too small in certain VM environments,
        # causing Chrome to fail or crash (see http://crbug.com/715363).
        # Use this flag to work-around this issue (a temporary directory
        # will always be used to create anonymous shared memory files).
        self.options.add_argument("--disable-dev-shm-usage")

        # Disables the sandbox for all process types that are normally
        # sandboxed. Meant to be used as a browser-level switch for testing
        # purposes only.
        self.options.add_argument("--no-sandbox")

        # Disables GPU hardware acceleration. If software renderer is not in
        # place, then the GPU process won't launch.
        self.options.add_argument("--disable-gpu")

        return self

    def set_proxy(self, proxy=None):
        # eğer isteniyorsa proxy işlemi başlat
        # eğer proxy kullanılmayacaksa koruma modunu devre dışı bırak
        # http://free-proxy.cz/en/proxylist/country/TR/all/speed/level1
        if not proxy:
            proxy = os.getenv("PROXY")

        self.options.add_argument(f"--proxy-server={proxy}")

        return self

    def mute_audio(self):
        self.options.add_argument("--mute-audio")

        return self

    def run(self):
        """
        Tarayıcıyı çalıştırır ve nesnesini döndürür

        :return: [WebDriver]
        """

        self.options.add_experimental_option(
            'excludeSwitches', self.excludeSwitches)

        self.driver = webdriver.Chrome(
            service=Service(DriverManager().install()),
            options=self.options
        )
        self.logger.info("Tarayıcı çalıştırıldı")

        return self

    def get(self) -> WebDriver:
        """
        :return: [WebDriver] webdriver tarayıcı nesnesini geri döndürür
        """

        if self.driver is None:
            return self.run().get()

        return self.driver

    def maximize_window(self):
        self.driver.maximize_window()

        return self

    def quit(self):
        self.close()

    def close(self):
        self.driver.close()
        self.driver = None

    def click(self, element: WebElement):
        try:
            element.click()
        except:
            self.driver.execute_script("arguments[0].click();", element)

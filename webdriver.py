from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
import urllib3
import logging


class Driver:
    """
    This class represents a Selenium web driver.

    Attributes:
        headless (bool): Indicates whether the driver should run in headless mode or not. Default is False.
        dir_dwld (str): The directory where downloaded files should be saved. Default is None.

    Methods:
        driver: Returns the initialized web driver.
        setup: Initializes and configures the web driver.
    """
    def __init__(self, headless=False, download_directory=None):
        self.headless = headless
        self.download_directory = download_directory
        self._driver = None

    @property
    def driver(self):
        """
       Property that returns the initialized web driver. If the driver is not initialized,
       it calls the setup method to initialize it.
       :return: The initialized web driver.
       """
        if self._driver is None:
            self._driver = self.setup()
        return self._driver

    def setup(self):
        """
        Initializes and configures the web driver. It sets up the necessary environment variables,
        configures the driver options, and returns the initialized driver.
        :return: The initialized web driver.
        """
        # Desativa os warnings de certificado SSL
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        # Configura as variáveis de ambiente
        os.environ['WDM_LOG'] = str(logging.NOTSET)
        os.environ['WDM_SSL_VERIFY'] = '0'
        # Configura as opções do driver
        options = Options()
        # Configura o driver para rodar em modo headless ou não
        if self.headless:
            options.add_argument('headless')
        if self.download_directory is not None:
            p = {'download.default_directory': self.download_directory}
            options.add_experimental_option('prefs', p)
        # Mantém o driver aberto após o término do script
        options.add_experimental_option("detach", True)
        # Desativa os logs do driver
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        # Configura o tamanho da janela do driver
        options.add_argument('--window-size=1920,1080')
        # Configura o idioma do driver
        options.add_argument("--lang=pt-BR")
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
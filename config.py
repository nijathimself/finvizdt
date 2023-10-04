##########driver configurations#########
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from webdriver_manager.utils import ChromeType
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import logging
import sys, os


LOGFILE = "testlog"
logging.basicConfig(filename=LOGFILE, 
                    format='%(asctime)s %(message)s', 
                    filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

class Config(object):
	"""docstring for Config"""
	def __init__(self):
		super(Config, self).__init__()
		self.driver = None
		self.wait_attrib = None
		self.logger = logger
		
	def drivers(self):	
		capa = DesiredCapabilities.CHROME
		capa["pageLoadStrategy"] = "none"
		options = Options()
		options.add_argument('--no-sandbox')
		options.add_argument('--disable-dev-shm-usage')
		options.add_argument('start-maximized')
		options.add_experimental_option("useAutomationExtension", False)
		options.add_experimental_option("excludeSwitches",["enable-automation"])
		options.add_argument("--incognito")
		options.add_argument("--headless")
		#options.headless = False
		

		options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
		service = Service(ChromeDriverManager().install(), chrome_options=options)
		#version="114.0.5735.90"
		#service = Service(executable_path=str(os.environ.get('CHROMEDRIVER_PATH')))
		self.driver = webdriver.Chrome(service=service, options=options)
		#self.driver = webdriver.Chrome(service=service, options=options)
		#self.driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=options,desired_capabilities=capa)
		#self.driver = webdriver.Chrome(executable_path=path_chrome,options=options,desired_capabilities=capa)
		#self.driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(),options=options,desired_capabilities=capa)
		# self.driver.delete_all_cookies()
		self.driver.maximize_window()
		return self.driver

	def wait(self):
		self.wait_attrib = WebDriverWait(self.driver, 20)
		return self.wait_attrib

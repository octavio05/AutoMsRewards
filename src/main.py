from dotenv import load_dotenv
from os import getenv
from selenium import webdriver
from msrewards.navigation import Navigation
from driverWrapper.wrapper import Wrapper
from shared.appLogging import AppLogging

# mobile_emulation = { "deviceName": "Pixel 5"}
# driver_options = webdriver.EdgeOptions()
# driver_options.add_experimental_option("mobileEmulation", mobile_emulation)

# driver = webdriver.Edge(driver_options)
logging = AppLogging()

logging.info('Process start')
print('Process start')

driver_options = webdriver.EdgeOptions()
driver_options.add_argument("--headless")
driver_options.add_argument("--no-sandbox")
driver_options.add_argument("--disable-dev-shm-usage")
driver_options.add_experimental_option("excludeSwitches", ["enable-logging"])

load_dotenv()

if (getenv('DEBUG_USER_DATA_DIR')):
    driver_options.add_argument(f"user-data-dir={getenv('DEBUG_USER_DATA_DIR')}")

driver = webdriver.Edge(options=driver_options)

logging.info('WebDriver created!')

driverWrapper = Wrapper(driver, logging)
nav = Navigation(driverWrapper, getenv('MAIL'), getenv('PASSWORD'), logging)

logging.info('Navigation start')

nav.start()

nav.login()

nav.checkCards()

nav.dailySearch()

logging.info('Process end')
print('Process end')
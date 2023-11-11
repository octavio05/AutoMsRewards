import logging
from appSecrets import MAIL, PASSWORD, DEBUG_USER_DATA_DIR
from selenium import webdriver
from msrewards.navigation import Navigation
from driverWrapper.wrapper import Wrapper

# mobile_emulation = { "deviceName": "Pixel 5"}
# driver_options = webdriver.EdgeOptions()
# driver_options.add_experimental_option("mobileEmulation", mobile_emulation)

# driver = webdriver.Edge(driver_options)
print("Enter app!")

# logging.basicConfig(filename="app.log", encoding="utf-8", level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

driver_options = webdriver.EdgeOptions()
driver_options.add_argument("--headless")
driver_options.add_argument("--no-sandbox")
driver_options.add_argument("--disable-dev-shm-usage")
driver_options.add_experimental_option("excludeSwitches", ["enable-logging"])

if (DEBUG_USER_DATA_DIR):
    driver_options.add_argument(f"user-data-dir={DEBUG_USER_DATA_DIR}")

driver = webdriver.Edge(options=driver_options)

# logging.info("Webdriver created!")
print("Webdriver created!")

driverWrapper = Wrapper(driver)
nav = Navigation(driverWrapper, MAIL, PASSWORD)

nav.start()

nav.login()

print("Logued!")
# logging.info("Logued!")

nav.checkCards()

print("Cards checked!")
# logging.info("Cards checked!")

#nav.dailySearch()

print("Do daily search!")
# logging.info("Do daily search!")

print("End of proccess")
# logging.info("End of proccess")
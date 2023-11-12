from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from shared.appLogging import AppLogging

class Wrapper:
    def __init__(self, driver: webdriver, logging: AppLogging) -> None:
        if (driver is None):
            raise ValueError('driver must be provided')
        
        if (logging is None):
            raise ValueError('logging must be provided')
        
        self.logging = logging
        self.driver = driver
        try:
            self.text = driver.text
        except AttributeError:
            self.Text = None

    def tryFindElement(self, cssSelectorValue:str):
        try:
            element = self.driver.find_element(by=By.CSS_SELECTOR, value=cssSelectorValue)
        except NoSuchElementException:
            element = None
        else:
            element = Wrapper(element, self.logging)

        return element is not None, element
    
    def findElement(self, cssSelectorValue:str):
        return Wrapper(self.driver.find_element(by=By.CSS_SELECTOR, value=cssSelectorValue), self.logging)
    
    def findElements(self, cssSelectorValue:str):
        return list(map(lambda x: 
            Wrapper(x, self.logging),
            self.driver.find_elements(by=By.CSS_SELECTOR, value=cssSelectorValue)   
        ))
    
    def click(self):
        self.driver.click()

    def tryClick(self, attempts = 1):
        doClick = False
        tryClick = 0

        while (not doClick and tryClick < attempts):
            try:
                self.driver.click()
            except Exception:
                doClick = False
            else:
                doClick = True
            finally:
                tryClick += 1
        
        return doClick
    
    def sendKeys(self, text:str):
        self.driver.send_keys(text)

    def clear(self):
        self.driver.clear()

    def get(self, url:str) -> None:
        # self.logging.info(f'Go to url {url}')
        self.driver.get(url)
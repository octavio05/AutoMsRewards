from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException

class Wrapper:
    def __init__(self, driver):
        if (driver is None):
            raise ValueError("driver must be provided")
        
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
            element = Wrapper(element)

        return element is not None, element
    
    def findElement(self, cssSelectorValue:str):
        return Wrapper(self.driver.find_element(by=By.CSS_SELECTOR, value=cssSelectorValue))
    
    def findElements(self, cssSelectorValue:str):
        #return self.driver.find_elements(by=By.CSS_SELECTOR, value=cssSelectorValue)
        return list(map(Wrapper, self.driver.find_elements(by=By.CSS_SELECTOR, value=cssSelectorValue)))
    
    def click(self):
        self.driver.click()

    def tryClick(self, attempts = 1):
        doClick = False
        tryClick = 0

        while (not doClick and tryClick < attempts):
            try:
                self.driver.click()
            except ElementNotInteractableException:
                doClick = False
            else:
                doClick = True
            finally:
                tryClick += 1
        
        return doClick
    
    def sendKeys(self, text:str):
        self.driver.send_keys(text)
import constants
from time import sleep

class TestManager:
    def isTestCard(self, cardText:str):
        cardText = cardText.lower()
        textToFind = ['test extra', 'test supersónico']

        for text in textToFind:
            if (text in cardText):
                return True
            
        return False   
    
    def isFastTestCard(self, cardText:str):
        return 'test a la velocidad de la luz' in cardText.lower()
    
    def resolveTest(self):
        self._closeAcceptCookieModal()

        exists, startTestButton = self.driverWrapper.tryFindElement(constants.START_TEST_BUTTON_CSS_SELECTOR)
        if (exists):
            startTestButton.click()

        totalPoints = int(self.driverWrapper.findElement(".rqPoints .rqMCredits").text)
        points = int(self.driverWrapper.findElement(".rqPoints .rqECredits").text)

        option = self._getNextTextExtraOptions()

        while (totalPoints != points):
            while(option is not None):
                try:
                    option.click()
                finally:
                    option = self._getNextTextExtraOptions()

            points += 10
            sleep(2)

    def resolveFastTest(self):
        self._closeAcceptCookieModal()

        exists, startTestButton = self.driverWrapper.tryFindElement(constants.START_TEST_BUTTON_CSS_SELECTOR)
        if (exists):
            startTestButton.click()     
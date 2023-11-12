from time import sleep
import random
import constants
from selenium.webdriver.common.keys import Keys
from driverWrapper.wrapper import Wrapper

from shared.appLogging import AppLogging

class Navigation:
    def __init__(self, driverWrapper: Wrapper, username:str, password:str, logging: AppLogging) -> None:
        if (driverWrapper is None):
            raise ValueError('driver must be provided')
        
        if (logging is None):
            raise ValueError('logging must be provided')

        self.username = username
        self.password = password
        self.driverWrapper = driverWrapper
        self.logging = logging
        self.tabBase = driverWrapper.driver.current_window_handle
        self.searchTerms = []

    def start(self) -> None:
        self.driverWrapper.get(constants.REWARDS_URL)

    def login(self) -> None:
        exists, loginInput = self.driverWrapper.tryFindElement(constants.LOGIN_INPUT_CSS_SELECTOR)
        if (exists):
            loginInput.sendKeys(self.username)
        else:
            self.logging.info('Already login')
            return

        submitButton = self.driverWrapper.findElement(constants.SUBMIT_BUTTON_CSS_SELECTOR)
        submitButton.click()

        sleep(1)

        passwordInput = self.driverWrapper.findElement(constants.PASSWORD_INPUT_CSS_SELECTOR)
        passwordInput.sendKeys(self.password)

        sleep(2)

        submitButton = self.driverWrapper.findElement(constants.SUBMIT_BUTTON_CSS_SELECTOR)
        submitButton.click()

        noSaveSessionButton = self.driverWrapper.findElement(constants.NO_SAVE_SESSION_BUTTON_CSS_SELECTOR)
        noSaveSessionButton.click()   

        self.logging.info('Login success')

    def _tryInternalLogin(self):
        exists, loginButton = self.driverWrapper.tryFindElement('.signInOptions .identityOption a')

        if (not exists):
            return
        
        sleep(constants.PREVENT_WAIT_SECONDS)
        
        loginButton.click()

        self.login()

    def checkCards(self) -> None:
        uncheckedCards = self._getUncheckedCards()
        if (not uncheckedCards):
            self.logging.info('All cards are checked')
            return
        
        self.logging.info(f'Find {len(uncheckedCards)} cards to check')

        for card in uncheckedCards:
            card.click()
            sleep(constants.PREVENT_WAIT_SECONDS)
            newTabId = self._tryGetNewTabId()

            if (self._isTestCard(card)):
                self.driverWrapper.driver.switch_to.window(newTabId) 
                sleep(1)  
                self.driverWrapper.driver.refresh()
                self._resolveTest()
            elif (self._isFastTestCard(card)):
                self.driverWrapper.driver.switch_to.window(newTabId) 
                sleep(1)  
                self.driverWrapper.driver.refresh()
                self._resolveFastTest()                

            self._closeTab(newTabId)
            sleep(constants.PREVENT_WAIT_SECONDS)

    def _closeAcceptCookieModal(self):
        exists, rejectCookieButton = self.driverWrapper.tryFindElement(constants.REJECT_COOKIE_BUTTON_CSS_SELECTOR)
        if (exists):
            sleep(1)
            rejectCookieButton.click()

    def _resolveTest(self):
        self._tryInternalLogin()
        self._closeAcceptCookieModal()

        exists, startTestButton = self.driverWrapper.tryFindElement(constants.START_TEST_BUTTON_CSS_SELECTOR)
        if (exists):
            startTestButton.tryClick(5)

        sleep(1)

        totalPoints = int(self.driverWrapper.findElement(constants.TEST_TOTAL_POINTS_CSS_SELECTOR).text)
        points = int(self.driverWrapper.findElement(constants.TEST_POINTS_CSS_SELECTOR).text)

        option = self._getNextTestOption()

        while (totalPoints != points):
            while(option is not None):
                try:
                    option.click()
                except Exception:
                    break
                else:
                    sleep(2)
                    option = self._getNextTestOption()

            points += 10
            sleep(4)

    def _resolveFastTest(self):
        self._closeAcceptCookieModal()

        exists, startTestButton = self.driverWrapper.tryFindElement(constants.START_TEST_BUTTON_CSS_SELECTOR)
        if (exists):
            startTestButton.tryClick(5)        

        totalPoints = int(self.driverWrapper.findElement(constants.TEST_TOTAL_POINTS_CSS_SELECTOR).text)
        points = totalPoints
        exists, pointsElement = self.driverWrapper.tryFindElement(constants.TEST_POINTS_CSS_SELECTOR)
        if (exists):
            points = int(pointsElement.text)

        option = self._getNextFastTestOption()  

        while(option is not None or totalPoints != points):
            try:
                option.click()
            except Exception:
                break
            finally:
                sleep(2)
                newPoints = int(self.driverWrapper.findElement(constants.TEST_POINTS_CSS_SELECTOR).text)
                if (points < newPoints):
                    sleep(2)
                points = newPoints
                option = self._getNextFastTestOption()

    def _getNextTestOption(self):
        elements = self.driverWrapper.findElements(constants.TEXT_EXTRA_OPTIONS_CSS_SELECTOR)

        if (not elements or self._areAllTestOptionsSuccess(elements)):
            return None

        for element in elements:
            exists, x = element.tryFindElement(constants.TEXT_EXTRA_OPTION_SELECTED_CSS_SELECTOR)
            if (exists):
                return element

    def _areAllTestOptionsSuccess(self, options):
        return list(filter(self._filterTestOptionsSuccess, options)).count == 5

    def _filterTestOptionsSuccess(self, option):
        exists, element = option.tryFindElement('img[data-bm="102"]')
        return exists
            
    def _getNextFastTestOption(self):
        elements = self.driverWrapper.findElements("#currentQuestionContainer .rq_button")

        if (not elements):
            return None
        
        for element in elements:
            exists, x = element.tryFindElement('.optionDisable')
            if (not exists):
                return element

    def dailySearch(self) -> None:
        try:
            pointsToComplete = self._getBrowserPointsToComplete()
        except AttributeError:
            # Mobile points
            pointsToComplete = 60

        if (pointsToComplete == 0):
            self.logging.info('All daily search points are completed')
            return
        
        self.logging.info(f'{pointsToComplete} daily search points to complete')

        self._tryLoginBing()

        for x in range(0, 0 if pointsToComplete == 0 else int(pointsToComplete/3) + 1):
            text = self._getRandomSearchTerm()
            self._doBingSearch(text)

            sleep(8)

    def _tryLoginBing(self):
        self.driverWrapper.get(constants.BING_URL)
        exists, bingLoginButton = self.driverWrapper.tryFindElement(constants.BING_LOGIN_BUTTON_CSS_SELECTOR)
        if (exists):
            sleep(1)
            self._closeAcceptCookieModal()
            sleep(1)
            bingLoginButton.click()   

    def _doBingSearch(self, value:str):
        inputText = self.driverWrapper.findElement('#sb_form_q')

        inputText.clear()
        inputText.sendKeys(value)
        inputText.sendKeys(Keys.RETURN)

    def _getBrowserPointsToComplete(self):
        exists, showDailyPointsLink = self.driverWrapper.tryFindElement(constants.SHOW_DAILY_POINTS_LINK_CSS_SELECTOR)
        if (not showDailyPointsLink.tryClick()):
            raise AttributeError("Element not clickable")

        allCardPoints = self.driverWrapper.findElements(constants.ALL_CARDS_POINTS_CSS_SELECTOR)

        totalCardPointsCompleted = 0
        totalCardPointsToComplete = 0
        cardPointTextForBrowsers = ["búsqueda en pc", "bonificación de microsoft edge"]
        for cardPoint in allCardPoints:
            if (cardPoint.findElement(constants.CARD_POINTS_TEXT_CSS_SELECTOR).text.lower() in cardPointTextForBrowsers):
                totalCardPointsCompleted += int(cardPoint.findElement(constants.POINTS_COMPLETED_CSS_SELECTOR).text)
                totalCardPointsToComplete += int(cardPoint.findElement(constants.POINTS_TO_COMPLETE_CSS_SELECTOR).text.split(" / ")[1])

        return totalCardPointsToComplete - totalCardPointsCompleted

    def _isTestCard(self, card):
        cardText = card.text.lower()
        textToFind = ['test extra', 'test supersónico']

        for text in textToFind:
            if (text in cardText):
                return True
            
        return False   
    
    def _isFastTestCard(self, card):
        cardText = card.text.lower()
        textToFind = ['test a la velocidad de la luz', 'preguntas sobre el navegador', 'desafío sobre rewards', 'cuestionario sobre microsoft']

        for text in textToFind:
            if (text in cardText):
                return True
            
        return False  

    def _tryGetNewTabId(self):
        tabs = list(filter(lambda x: (x != self.tabBase), self.driverWrapper.driver.window_handles))

        return None if (len(tabs) == 0) else tabs[0]

    def _closeTab(self, tabId):
        if (tabId is None):
            return
        
        self.driverWrapper.driver.switch_to.window(tabId)
        sleep(1)
        self.driverWrapper.driver.close()
        self.driverWrapper.driver.switch_to.window(self.tabBase)          

    def _getCards(self):
        return self.driverWrapper.findElements("mee-card")

    def _isUncheckedCard(self, card):
        exists, element = card.tryFindElement(".mee-icon-AddMedium")

        return exists

    def _getUncheckedCards(self) -> list:
        cards = self._getCards()

        return list(filter(self._isUncheckedCard, cards))

    def _getRandomSearchTerm(self):
        if (not self.searchTerms):
            self.searchTerms = constants.SEARCH_TERMS.copy()

        randomTerm = random.choice(self.searchTerms)
        self.searchTerms.remove(randomTerm)

        return randomTerm
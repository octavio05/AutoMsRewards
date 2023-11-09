from time import sleep
import random
import constants

class Navigation:
    def __init__(self, driverWrapper, username:str, password:str):
        if (driverWrapper is None):
            raise ValueError("driver must be provided")
        
        self.username = username
        self.password = password
        self.driverWrapper = driverWrapper
        self.tabBase = driverWrapper.driver.current_window_handle

    def start(self):
        self.driverWrapper.driver.get(constants.REWARDS_URL)

    def login(self):
        exists, loginInput = self.driverWrapper.tryFindElement(constants.LOGIN_INPUT_CSS_SELECTOR)
        if (exists):
            loginInput.sendKeys(self.username)
        else:
            print("already loged in")
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
        
    def _tryInternalLogin(self):
        exists, loginButton = self.driverWrapper.tryFindElement('.signInOptions .identityOption a')

        if (not exists):
            return
        
        sleep(constants.PREVENT_WAIT_SECONDS)
        
        loginButton.click()

        self.login()

    def checkCards(self):
        uncheckedCards = self._getUncheckedCards()
        if (not uncheckedCards):
            return
        
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

        totalPoints = int(self.driverWrapper.findElement(".rqPoints .rqMCredits").text)
        points = int(self.driverWrapper.findElement(".rqPoints .rqECredits").text)

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

        totalPoints = int(self.driverWrapper.findElement(".rqPoints .rqMCredits").text)
        points = int(self.driverWrapper.findElement(".rqPoints .rqECredits").text)    

        option = self._getNextFastTestOption()  

        while(option is not None or totalPoints != points):
            try:
                option.click()
            except Exception:
                break
            finally:
                sleep(2)
                points = int(self.driverWrapper.findElement(".rqPoints .rqMCredits").text)
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

    def dailySearch(self):
        try:
            pointsToComplete = self._getBrowserPointsToComplete()
        except AttributeError:
            # Mobile points
            pointsToComplete = 60

        if (pointsToComplete == 0):
            return
        
        self._tryLoginBing()

        for x in range(0, 0 if pointsToComplete == 0 else int(pointsToComplete/3) + 1):
            randomNumber = random.randrange(1, 500)
            self._doBingSearch(randomNumber)

            sleep(8)

    def _tryLoginBing(self):
        self.driverWrapper.driver.get(constants.BING_URL)
        exists, bingLoginButton = self.driverWrapper.tryFindElement(constants.BING_LOGIN_BUTTON_CSS_SELECTOR)
        if (exists):
            sleep(1)
            self._closeAcceptCookieModal()
            sleep(1)
            bingLoginButton.click()   

    def _doBingSearch(self, value:str):
        self.driverWrapper.driver.get(constants.BING_SEARCH_URL.format(value))    

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
        return 'test a la velocidad de la luz' in card.text.lower()

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

    def _getUncheckedCards(self):
        # return self.driverWrapper.findElements(constants.UNCHECKED_CARDS_CSS_SELECTOR)
        cards = self._getCards()

        return list(filter(self._isUncheckedCard, cards))

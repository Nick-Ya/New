from appium.webdriver.common.appiumby import AppiumBy

class CalculatorPage:
    def __init__(self, driver):
        self.driver = driver

    def click_7(self):
        self.driver.find_element(AppiumBy.ID, "com.apps.calculator.thecalculator:id/btn_7").click()

    def click_plus(self):
        self.driver.find_element(AppiumBy.ID, "com.apps.calculator.thecalculator:id/btn_plus").click()

    def click_9(self):
        self.driver.find_element(AppiumBy.ID, "com.apps.calculator.thecalculator:id/btn_9").click()

    def click_equals(self):
        self.driver.find_element(AppiumBy.ID, "com.apps.calculator.thecalculator:id/btn_equals").click()

    def get_result(self):
        return self.driver.find_element(AppiumBy.ID, "com.apps.calculator.thecalculator:id/result").text.strip()

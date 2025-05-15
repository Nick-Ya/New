import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options

@pytest.fixture(scope="function")
def driver():
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = "EE438L006710"
    options.platform_version = "15"
    options.app_package = "com.apps.calculator.thecalculator"
    options.app_activity = "com.example.icaculator.MainActivity"
    options.no_reset = True

    driver = webdriver.Remote("http://localhost:4723", options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

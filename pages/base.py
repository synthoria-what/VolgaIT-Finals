from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver

class BasePage:
    def __init__(self, browser: WebDriver):
        self.browser = browser
        self.base_url = "https://demoqa.com"

    def find_element(self, locator, time: int = 10):
        return WebDriverWait(self.browser, time).until(
            EC.presence_of_element_located(locator), message=f"Can't find element by locator {locator}"
        )

    def find_elements(self, locator, time: int = 10):
        return WebDriverWait(self.browser, time).until(
            EC.presence_of_all_elements_located(locator), message=f"Can't find element by locator {locator}"
        )

    def go_to_site(self):
        return self.browser.get(self.base_url)
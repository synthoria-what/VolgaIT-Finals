import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base import BasePage
from pages.locators import DemoQABookDetailsHelper


class BookDetailsPage(BasePage):
    def get_book_title(self):
        title = self.find_element(
            DemoQABookDetailsHelper.LOCATOR_BOOK_TITLE
        )
        return title.text

    def add_book(self):
        locator = DemoQABookDetailsHelper.LOCATOR_ADD_BOOK_BUTTON

        button = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable(locator)
        )

        self.browser.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            button
        )

        button.click()

        alert = WebDriverWait(self.browser, 20).until(
            EC.alert_is_present()
        )

        message = alert.text
        alert.accept()

        return message

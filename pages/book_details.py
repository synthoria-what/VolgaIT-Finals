import time

import allure
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
        with allure.step(f"Пробуем добавить книгу в профиль"):
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

    def is_add_button_available(self):
        # Сначала ждём загрузки карточки, чтобы отсутствие кнопки было значимым.
        WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located(DemoQABookDetailsHelper.LOCATOR_BOOK_TITLE)
        )
        return any(element.is_displayed() and element.is_enabled()
                   for element in self.browser.find_elements(
                       *DemoQABookDetailsHelper.LOCATOR_ADD_BOOK_BUTTON))

    def has_login_button(self):
        return self.find_element(DemoQABookDetailsHelper.LOCATOR_LOGIN_BUTTON).is_displayed()

    @allure.step("Вернуться из карточки в книжный магазин")
    def back_to_store(self):
        self.click(DemoQABookDetailsHelper.LOCATOR_BACK_TO_STORE)

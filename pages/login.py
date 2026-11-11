import allure

from pages.base import BasePage
from pages.locators import DemoQALoginHelper
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class LoginPage(BasePage):

    def open_login_page(self):
        with allure.step("Открываем форму авторизации"):
            self.browser.get(f"{self.base_url}/login")

    def enter_username(self, username: str):
        with allure.step(f"Вводим данные: {username}"):
            username_field = self.find_element(
                DemoQALoginHelper.LOCATOR_LOGIN_USERNAME_FIELD
            )
            username_field.send_keys(username)

    def enter_password(self, password: str):
        with allure.step(f"Вводим данные: {password}"):
            password_field = self.find_element(
                DemoQALoginHelper.LOCATOR_LOGIN_PASSWORD_FIELD
            )
            password_field.send_keys(password)

    def click_login(self):
        with allure.step(f"Нажимаем кнопку авторизации"):
            login_button = self.find_element(
                DemoQALoginHelper.LOCATOR_SUBMIT_BUTTON
            )
            login_button.click()

    def login(self, username: str, password: str):
        with allure.step(f"Авторизация..."):
            self.enter_username(username)
            self.enter_password(password)
            self.click_login()

    def clear(self):
        username_field = self.find_element(
            DemoQALoginHelper.LOCATOR_LOGIN_USERNAME_FIELD
        )
        username_field.clear()

        password_field = self.find_element(
            DemoQALoginHelper.LOCATOR_LOGIN_PASSWORD_FIELD
        )
        password_field.clear()

    def get_error_message(self):
        locator = DemoQALoginHelper.LOCATOR_ERROR_MESSAGE

        WebDriverWait(self.browser, 10).until(
            EC.text_to_be_present_in_element(
                locator, "Invalid username or password!"
            )
        )
        return self.find_element(locator).text

    def get_profile_username(self):
        return self.find_element(
            DemoQALoginHelper.LOCATOR_PROFILE_USERNAME
        ).text


    
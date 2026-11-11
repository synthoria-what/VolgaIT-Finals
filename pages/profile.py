from pages.base import BasePage
from selenium.webdriver.common.by import By


class ProfilePage(BasePage):
    def open_profile(self):
        self.browser.get(f"{self.base_url}/profile")

    def get_books(self):
            table = self.find_element(
                (By.CSS_SELECTOR, ".rt-tbody")
            )

            books = table.find_elements(
                By.CSS_SELECTOR, ".rt-tr-group a"
            )

            return [book.text for book in books if book.text]
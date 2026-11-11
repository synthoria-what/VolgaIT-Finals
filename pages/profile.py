import allure
from selenium.common import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base import BasePage
from selenium.webdriver.common.by import By
from pages.locators import DemoQAProfileHelper

class ProfilePage(BasePage):
    def open_profile(self):
        self.browser.get(f"{self.base_url}/profile")

    def get_books(self):
        with allure.step(f"Получаем книги"):
            table = self.find_element(DemoQAProfileHelper.LOCATOR_PROFILE_TABLE)

            books = table.find_elements(*DemoQAProfileHelper.LOCATOR_PROFILE_BOOK_ROWS)

            return [book.text for book in books if book.text]

    def is_book_added(self, book_title: str) -> bool:
        try:
            WebDriverWait(self.browser, 10).until(
                EC.visibility_of_element_located((By.LINK_TEXT, book_title))
            )
            return True
        except TimeoutException:
            return False

    # def get_book(self, title: str) -> list[str]:
    #     self.find_element(self.BOOK_TABLE, 20)
    #     rows = self.browser.find_elements(*self.BOOK_ROWS)
    #
    #     for row in rows:
    #         links = row.find_elements(By.TAG_NAME, "a")
    #
    #         for link in links:
    #             book_title = link.text.strip()
    #
    #             if book_title == title:
    #                 return [book_title]
    #
    #     return []
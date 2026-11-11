from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base import BasePage


class BookStorePage(BasePage):

    SEARCH_FIELD = (By.ID, "searchBox")
    BOOK_TABLE = (By.CSS_SELECTOR, ".rt-tbody")
    BOOK_ROWS = (By.CSS_SELECTOR, ".rt-tbody .rt-tr-group")

    def open_book_store(self):
        self.browser.get(f"{self.base_url}/books")

        WebDriverWait(self.browser, 20).until(
            EC.presence_of_element_located(self.SEARCH_FIELD)
        )

        WebDriverWait(self.browser, 20).until(
            EC.presence_of_element_located(self.BOOK_TABLE)
        )

    def get_books(self):
        self.find_element(self.BOOK_TABLE, 20)

        rows = self.browser.find_elements(*self.BOOK_ROWS)

        books = []

        for row in rows:
            links = row.find_elements(By.TAG_NAME, "a")

            for link in links:
                title = link.text.strip()

                if title:
                    books.append(title)

        return books

    def search_book(self, title: str):
        search_field = self.find_element(self.SEARCH_FIELD)

        search_field.clear()
        search_field.send_keys(title)

    def open_book(self, title: str):
        book = self.find_element((By.LINK_TEXT, title))
        book.click()


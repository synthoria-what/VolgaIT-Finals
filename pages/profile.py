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

    def wait_for_username(self, username):
            WebDriverWait(self.browser, 15).until(
                EC.text_to_be_present_in_element(DemoQAProfileHelper.LOCATOR_USERNAME, username)
            )
            assert self.find_element(DemoQAProfileHelper.LOCATOR_USERNAME).text == username

    @allure.step("Дождаться списка книг: {titles}")
    def wait_for_books(self, titles):
        # Пустая таблица появляется до ответа API. Дожидаемся завершения fetch,
        # иначе его поздний ответ может сбросить только что открытый диалог.
        WebDriverWait(self.browser, 15).until(
            lambda driver: driver.execute_script("""
                return performance.getEntriesByType('resource').some(entry =>
                    new URL(entry.name).pathname.startsWith('/Account/v1/User/')
                    && entry.responseEnd > 0);
            """),
            message="Не завершилась загрузка профиля из API",
        )
        WebDriverWait(self.browser, 15).until(
            lambda _: sorted(self.get_books()) == sorted(titles),
            message=f"Ожидались книги в профиле: {titles}",
        )
        return self.get_books()

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

    @allure.step("Проверить сообщение о необходимости авторизации")
    def get_guest_message(self):
        return WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located(DemoQAProfileHelper.LOCATOR_NOT_LOGGED_IN)
        ).text

    def has_collection_controls(self):
        locators = [DemoQAProfileHelper.LOCATOR_SEARCH_FIELD, DemoQAProfileHelper.LOCATOR_DELETE_ALL,
                    DemoQAProfileHelper.LOCATOR_BOOK_LINKS]
        return any(element.is_displayed() for locator in locators
                   for element in self.browser.find_elements(*locator))

    @allure.step("Выйти из профиля")
    def logout(self):
        self.click(DemoQAProfileHelper.LOCATOR_LOGOUT)
        WebDriverWait(self.browser, 10).until(EC.url_contains("/login"))

    @allure.step("Перейти из профиля в книжный магазин")
    def go_to_book_store(self):
        self.click(DemoQAProfileHelper.LOCATOR_GO_TO_STORE)
        WebDriverWait(self.browser, 10).until(EC.url_contains("/books"))

    @allure.step("Удалить из профиля книгу: {title}")
    def delete_book(self, title):
        link = self.find_element((By.LINK_TEXT, title))
        row = link.find_element(By.XPATH, "ancestor::tr")
        delete_button = row.find_element(By.CSS_SELECTOR, "[id^='delete-record-']")
        isbn = delete_button.get_attribute("id").removeprefix("delete-record-")
        assert self.request_deletion("book", isbn) == "Delete Book"
        return self.confirm_deletion()

    @allure.step("Открыть подтверждение удаления: {target}")
    def request_deletion(self, target, isbn=None):
        locator = ((By.ID, f"delete-record-{isbn}") if target == "book"
                   else DemoQAProfileHelper.LOCATOR_DELETE_ALL)
        self.click(locator)
        WebDriverWait(self.browser, 10).until(
            EC.visibility_of_element_located(DemoQAProfileHelper.LOCATOR_MODAL)
        )
        return self.find_element(DemoQAProfileHelper.LOCATOR_MODAL_TITLE).text

    @allure.step("Отменить удаление книг")
    def cancel_deletion(self):
        self.click(DemoQAProfileHelper.LOCATOR_MODAL_CANCEL)
        WebDriverWait(self.browser, 10).until(
            EC.invisibility_of_element_located(DemoQAProfileHelper.LOCATOR_MODAL)
        )

    @allure.step("Подтвердить удаление и прочитать предупреждение")
    def confirm_deletion(self):
        self.click(DemoQAProfileHelper.LOCATOR_MODAL_CONFIRM)
        alert = WebDriverWait(self.browser, 10).until(EC.alert_is_present())
        message = alert.text
        alert.accept()
        return message

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
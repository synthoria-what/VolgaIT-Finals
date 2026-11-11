import pytest
import allure

from pages.book_store import BookStorePage
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.login import LoginPage
from pages.book_details import BookDetailsPage
from pages.profile import ProfilePage

@pytest.mark.ui
@pytest.mark.positive
@allure.title("UI1 - Отображение списка книг")
def test_get_books(browser):

    book_store = BookStorePage(browser)

    book_store.open_book_store()

    books = book_store.get_books()

    assert len(books) > 0
    assert "Git Pocket Guide" in books

@pytest.mark.ui
@pytest.mark.positive
@allure.title("UI-02 - Поиск книги по названию")
def test_search_book(browser):

    book_store = BookStorePage(browser)

    book_store.open_book_store()

    book_store.search_book("Git Pocket Guide")

    books = WebDriverWait(browser, 10).until(
        lambda driver: book_store.get_books()
        == ["Git Pocket Guide"]
    )

    assert books == ["Git Pocket Guide"]

@pytest.mark.ui
@pytest.mark.positive
@allure.title("UI-03 - Добавление книги через интерфейс")
def test_add_book_ui(browser, api_user):
    login_page = LoginPage(browser)
    book_store = BookStorePage(browser)
    book_details = BookDetailsPage(browser)
    profile_page = ProfilePage(browser)

    # Авторизация
    login_page.open_login_page()

    login_page.login(
        api_user["username"],
        api_user["password"]
    )

    WebDriverWait(browser, 15).until(
        EC.url_contains("/profile")
    )

    book_store.open_book_store()

    books = book_store.get_books()

    assert len(books) > 0

    book_title = books[0]

    book_store.open_book(book_title)

    message = book_details.add_book()

    assert message == "Book added to your collection."

    profile_page.open_profile()

    assert profile_page.is_book_added(book_title)
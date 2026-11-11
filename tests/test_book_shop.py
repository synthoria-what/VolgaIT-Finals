import pytest
import allure

from pages.book_store import BookStorePage
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.login import LoginPage
from pages.book_details import BookDetailsPage
from pages.profile import ProfilePage

pytestmark = [
    allure.parent_suite("DemoQA Тестирование"),
    allure.suite("Страница маганиза книг"),
]

@pytest.mark.ui
@pytest.mark.positive
@allure.title("Отображение списка книг")
def test_get_books(browser):

    book_store = BookStorePage(browser)

    with allure.step("Открываем книжный магазин"):
        book_store.open_book_store()

    with allure.step("Получаем книги"):
        books = book_store.get_books()

    assert len(books) > 0
    assert "Git Pocket Guide" in books

@pytest.mark.ui
@pytest.mark.positive
@allure.title("Поиск книги по названию")
def test_search_book(browser):

    book_store = BookStorePage(browser)

    with allure.step("Открывем книжный магазин"):
        book_store.open_book_store()

    book_store.search_book("Git Pocket Guide")

    book = book_store.get_book("Git Pocket Guide")

    assert book == ["Git Pocket Guide"]

@pytest.mark.ui
@pytest.mark.positive
@allure.title("Добавление книги через интерфейс")
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

    assert profile_page.is_book_added(book_title) == True

@pytest.mark.ui
@pytest.mark.negative
@pytest.mark.parametrize("query", [
    pytest.param("no_such_book_9f3a72", id="unknown-title"),
    pytest.param("!@#$%^&*()", id="special-characters"),
    pytest.param("x" * 256, id="long-query"),
])
@allure.title("Поиск без совпадений и восстановление каталога")
def test_search_without_matches(browser, query):
    store = BookStorePage(browser)
    store.open_book_store()
    original_books = store.get_books()
    assert original_books

    store.search_book(query)
    assert store.wait_for_books([]) == []

    store.search_book("")
    assert sorted(store.wait_for_books(original_books)) == sorted(original_books)

@pytest.mark.ui
@pytest.mark.negative
@allure.title("Гость не может добавить книгу в коллекцию")
def test_guest_cannot_add_book(browser):
    store = BookStorePage(browser)
    details = BookDetailsPage(browser)
    store.open_book_store()
    title = store.get_books()[0]
    store.open_book(title)

    assert details.get_book_title() == title
    assert not details.is_add_button_available()
    assert details.has_login_button()

@pytest.mark.ui
@pytest.mark.negative
@allure.title("Повторное добавление книги не меняет коллекцию")
def test_duplicate_book_is_rejected(browser, user_with_books):
    user = user_with_books
    store = BookStorePage(browser)
    details = BookDetailsPage(browser)
    profile = ProfilePage(browser)
    book = user["books"][0]
    store.open_book_store()
    store.open_book(book["title"])

    assert details.add_book() == "Book already present in the your collection!"

    response = user["api"].get_user(user["user_id"])
    assert response.status_code == 200, response.text
    expected_isbns = sorted(book["isbn"] for book in user["books"])
    assert sorted(book["isbn"] for book in response.json()["books"]) == expected_isbns
    profile.open_profile()
    titles = [book["title"] for book in user["books"]]
    assert sorted(profile.wait_for_books(titles)) == sorted(titles)
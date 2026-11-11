import allure
import pytest

from pages.book_details import BookDetailsPage
from pages.book_store import BookStorePage
from pages.login import LoginPage
from pages.profile import ProfilePage


pytestmark = [
    pytest.mark.e2e,
    pytest.mark.positive,
    allure.suite("End-to-end: профиль и книжный магазин"),
]


@allure.step("Войти через UI под созданным пользователем")
def login_via_ui(browser, user):
    login = LoginPage(browser)
    login.open_login_page()
    login.login(user["username"], user["password"])
    profile = ProfilePage(browser)
    profile.wait_for_username(user["username"])
    token = browser.get_cookie("token")
    assert token and token["value"], "После UI-входа отсутствует токен"
    user["api"].set_token(token["value"])
    return profile


@allure.step("Получить каталог через API")
def get_catalog(api):
    response = api.get_books()
    assert response.status_code == 200, response.text
    books = response.json()["books"]
    assert isinstance(books, list)
    assert len(books) >= 3, "Для E2E-сценария нужны три книги в каталоге"
    assert len({book["isbn"] for book in books}) == len(books)
    return books


@allure.step("Добавить три книги через API")
def add_three_books(user, books):
    isbns = [book["isbn"] for book in books]
    assert len(isbns) == 3
    response = user["api"].add_books(user["user_id"], isbns)
    assert response.status_code == 201, response.text
    assert sorted(book["isbn"] for book in response.json()["books"]) == sorted(isbns)


@allure.step("Проверить точный состав коллекции через API")
def assert_api_collection(user, expected_books):
    response = user["api"].get_user(user["user_id"])
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["userId"] == user["user_id"]
    assert data["username"] == user["username"]
    assert isinstance(data["books"], list)
    assert sorted(book["isbn"] for book in data["books"]) == sorted(
        book["isbn"] for book in expected_books
    )


@pytest.mark.ui
@allure.title("E2E UI: добавить три книги, удалить одну и получить список из профиля")
def test_e2e_ui_collection_lifecycle(browser, api_user):
    profile = login_via_ui(browser, api_user)
    profile.wait_for_books([])
    store = BookStorePage(browser)
    details = BookDetailsPage(browser)

    with allure.step("Перейти в магазин и выбрать три книги из каталога"):
        profile.go_to_book_store()
        # Дожидаемся непустого каталога после перехода из профиля.
        store.find_elements(store.BOOK_LINKS, 20)
        catalog_titles = store.get_books()
        assert len(catalog_titles) >= 3
        titles = catalog_titles[:3]

    with allure.step("Добавить каждую из трёх книг через карточку в UI"):
        for title in titles:
            store.open_book(title)
            assert details.get_book_title() == title
            assert details.add_book() == "Book added to your collection."
            details.back_to_store()
            store.wait_for_books(catalog_titles)

    with allure.step("Открыть профиль и проверить все три книги"):
        profile.open_profile()
        profile.wait_for_books(titles)

    with allure.step("Удалить вторую книгу через UI"):
        assert profile.delete_book(titles[1]) == "Book deleted."
        remaining = [titles[0], titles[2]]
        profile.wait_for_books(remaining)

    with allure.step("Повторно открыть профиль и проверить сохранённые две книги"):
        profile.open_profile()
        assert sorted(profile.wait_for_books(remaining)) == sorted(remaining)


@pytest.mark.api
@allure.title("E2E API: добавить три книги, удалить одну и получить список из профиля")
def test_e2e_api_collection_lifecycle(api_user):
    user = api_user
    api = user["api"]

    with allure.step("Авторизоваться и получить токен через API"):
        response = api.authorize(user["username"], user["password"])
        assert response.status_code == 200, response.text
        assert response.json() is True
        response = api.generate_token(user["username"], user["password"])
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["status"] == "Success", response.text
        assert data["token"]
        api.set_token(data["token"])

    assert_api_collection(user, [])
    catalog = get_catalog(api)
    books = catalog[:3]
    add_three_books(user, books)
    assert_api_collection(user, books)

    with allure.step("Удалить вторую книгу через API"):
        response = api.delete_book(user["user_id"], books[1]["isbn"])
        assert response.status_code == 204, response.text
        assert not response.content

    assert_api_collection(user, [books[0], books[2]])

    with allure.step("Убедиться, что удаление из профиля не изменило каталог"):
        current_catalog = get_catalog(api)
        assert sorted(book["isbn"] for book in current_catalog) == sorted(
            book["isbn"] for book in catalog
        )


@pytest.mark.ui
@pytest.mark.api
@allure.title("E2E API + UI: добавить три книги, удалить одну и проверить повторный вход")
def test_e2e_api_add_ui_delete_and_relogin(browser, api_user):
    user = api_user
    profile = login_via_ui(browser, user)
    profile.wait_for_books([])
    store = BookStorePage(browser)

    with allure.step("Перейти в магазин и сверить выбранные книги с UI"):
        profile.go_to_book_store()
        store.find_elements(store.BOOK_LINKS, 20)
        books = get_catalog(user["api"])[:3]
        assert all(book["title"] in store.get_books() for book in books)

    add_three_books(user, books)
    assert_api_collection(user, books)

    with allure.step("Проверить в UI три книги, добавленные через API"):
        profile.open_profile()
        profile.wait_for_books([book["title"] for book in books])

    with allure.step("Удалить третью книгу через UI и проверить результат в API"):
        assert profile.delete_book(books[2]["title"]) == "Book deleted."
        remaining = books[:2]
        titles = [book["title"] for book in remaining]
        profile.wait_for_books(titles)
        assert_api_collection(user, remaining)

    with allure.step("Выйти, войти заново и проверить сохранённую коллекцию"):
        profile.logout()
        profile = login_via_ui(browser, user)
        assert sorted(profile.wait_for_books(titles)) == sorted(titles)
        assert_api_collection(user, remaining)

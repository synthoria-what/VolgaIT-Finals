

import uuid

import allure
import pytest
from selenium import webdriver

from api.book_store_api import BookStoreApi


@pytest.fixture
def browser():
    options = webdriver.ChromeOptions()

    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1920, 1080)
    yield driver

    driver.quit()

@pytest.fixture
def api_client():
    api = BookStoreApi()

    yield api

    api.close()

@pytest.fixture
def anonymous_api():
    # Апи пользователь без авторизации
    client = BookStoreApi()
    yield client
    client.close()

@pytest.fixture(scope="function")
def api_user(api_client):
    username = f"qa_{uuid.uuid4().hex[:10]}"
    password = "Test123!@#"

    create_response = api_client.create_user(
        username, password
    )

    assert create_response.status_code == 201, (
        create_response.text
    )

    user_id = create_response.json()["userID"]

    token = None

    try:
        token_response = api_client.generate_token(
            username, password
        )

        assert token_response.status_code == 200, (
            token_response.text
        )

        token = token_response.json()["token"]

        assert token

        api_client.set_token(token)

        yield {
            "api": api_client,
            "username": username,
            "password": password,
            "user_id": user_id,
            "token": token
        }

    finally:
        if token:
            api_client.delete_user(user_id)

@pytest.fixture
def api_user_with_books(api_user):
    api = api_user["api"]
    response = api.get_books()
    assert response.status_code == 200, response.text
    books = response.json()["books"][:2]
    assert len(books) == 2, "Для теста нужны две книги в каталоге"
    for book in books:
        response = api.add_book(api_user["user_id"], book["isbn"])
        assert response.status_code == 201, response.text
    return {**api_user, "books": books}


@pytest.fixture
def user_with_books(api_user_with_books, logged_in_user):
    return {**logged_in_user, "books": api_user_with_books["books"]}

class DemoQAUser:
    username: str = "Synthoria"
    password: str = "Synthoria123@!"


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    # Делаем скриншот только если упал сам тест (фаза 'call')
    if rep.when == "call" and rep.failed:
        # Пример для Playwright (если используете фикстуру page)
        page = item.funcargs.get("page")
        if page:
            allure.attach(
                page.screenshot(),
                name="Скриншот при падении",
                attachment_type=allure.attachment_type.PNG
            )
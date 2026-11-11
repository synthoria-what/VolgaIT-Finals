

import uuid

import allure
import pytest
from selenium import webdriver

from api.book_store_api import BookStoreApi
from pages.login import LoginPage
from pages.profile import ProfilePage


def pytest_addoption(parser):
    parser.addoption("--headless", action="store_true", help="Run Chrome without a window")
    parser.addoption("--no-sandbox", action="store_true", help="For isolated CI containers")
    parser.addoption("--browser-binary", help="Path to Chrome/Chromium")
    parser.addoption("--browser-proxy", help="HTTP proxy for the test browser")


@pytest.fixture
def browser(request):
    options = webdriver.ChromeOptions()
    if request.config.getoption("--headless"):
        options.add_argument("--headless=new")
    if request.config.getoption("--no-sandbox"):
        options.add_argument("--no-sandbox")
    if request.config.getoption("--browser-binary"):
        options.binary_location = request.config.getoption("--browser-binary")
    if request.config.getoption("--browser-proxy"):
        options.add_argument("--proxy-server=" + request.config.getoption("--browser-proxy"))
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)

    driver.set_window_size(1920, 1080)
    driver.set_page_load_timeout(30)
    try:
        yield driver
    finally:
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
            response = api_client.delete_user(user_id)
            if response.status_code == 401:
                # UI-вход мог заменить токен, полученный при создании пользователя.
                token_response = api_client.generate_token(username, password)
                assert token_response.status_code == 200, token_response.text
                cleanup_token = token_response.json().get("token")
                assert cleanup_token, "Не удалось получить токен для удаления тестового пользователя"
                api_client.set_token(cleanup_token)
                response = api_client.delete_user(user_id)
            assert response.status_code in (204, 404), response.text


class DemoQAUser:
    username: str = "Synthoria"
    password: str = "Synthoria123@!"


@pytest.fixture
def logged_in_user(browser, api_user):
    login = LoginPage(browser)
    login.open_login_page()
    login.login(api_user["username"], api_user["password"])
    ProfilePage(browser).wait_for_username(api_user["username"])
    # UI-вход выпускает новый токен и заменяет токен, полученный при API-подготовке.
    token = browser.get_cookie("token")
    assert token and token["value"], "После UI-входа отсутствует cookie token"
    api_user["api"].set_token(token["value"])
    api_user["token"] = token["value"]
    return api_user


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


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    # Делаем скриншот только если упал сам тест (фаза 'call')
    if rep.when == "call" and rep.failed:
        browser = item.funcargs.get("browser")
        if browser:
            allure.attach(
                browser.get_screenshot_as_png(),
                name="Скриншот при падении",
                attachment_type=allure.attachment_type.PNG
            )

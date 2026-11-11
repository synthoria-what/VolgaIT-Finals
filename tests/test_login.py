import pytest
import allure
from pages.login import LoginPage
from conftest import DemoQAUser

@pytest.mark.ui
@pytest.mark.positive
@allure.title("LOGIN-PAGE1 - Успешный вход в профиль")
def test_successful_login(browser):
    login_page = LoginPage(browser)
    login_page.open_login_page()
    login_page.login(DemoQAUser.username, DemoQAUser.password)

    assert login_page.get_profile_username() == "Synthoria"

@pytest.mark.ui
@pytest.mark.positive
@allure.title("LOGIN-PAGE2 - Пользователь забыл указать один символ в данных и повторил запрос")
def test_forgot_one_letter(browser):
    login_page = LoginPage(browser)
    login_page.open_login_page()
    login_page.login("Synthori", "Synthoria123@!")

    assert login_page.get_error_message() == \
            "Invalid username or password!"
    
    login_page.login("a", "")

    assert login_page.get_profile_username() == DemoQAUser.username

@pytest.mark.ui
@pytest.mark.negative
@allure.title("LOGIN-PAGE3 - Ввод не правильных данных")
def test_invalid_login(browser):
    login_page = LoginPage(browser)
    login_page.open_login_page()
    login_page.login("wrong_user", "wrong_password")

    assert login_page.get_error_message() == \
        "Invalid username or password!"


@pytest.mark.parametrize(
    "username, password",
    [
        ("unknown_user_12345", "WrongPassword123"),
        ("admin", "wrong_password"),
        ("test_user_99999", "123456"),
    ]
)
@pytest.mark.ui
@pytest.mark.negative
@allure.title("LOGIN-04 - Авторизация с неверными данными")
def test_invalid_credentials(browser, username, password):
    login_page = LoginPage(browser)
    login_page.open_login_page()
    login_page.login(username, password)

    assert login_page.get_error_message() == (
        "Invalid username or password!"
    )

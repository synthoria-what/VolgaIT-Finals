import uuid
import pytest
import allure



pytestmark = [
    pytest.mark.negative,
    pytest.mark.api,
    allure.suit("API"),
    allure.parent_suite("DemoQA Тестирование")
]

@allure.step("Проверить HTTP-статус и JSON ошибки")
def assert_error(response, status, code, message):
    assert response.status_code == status, response.text
    assert response.json() == {"code": code, "message": message}, response.text

@allure.step("Получить первый номер книги")
def get_first_isbn(api):
    response = api.get_books()
    assert response.status_code == 200, response.text
    books = response.json()["books"]
    assert books, "Book Store returned an empty catalog"
    return books[0]["isbn"]

@allure.title("Несуществующий ISBN")
def test_get_book_invalid_isbn(api_client):
    response = api_client.get_book("0000000000000")

    assert_error(response, 400, "1205", "ISBN supplied is not available in Books Collection!",)

@allure.title("Ошибка авторизации")
def test_invalid_authorized_user(api_user):
    response = api_user["api"].authorize(
        api_user["username"] + "jjj",
        api_user["password"],
    )

    assert_error(response, 404, "1207", "User not found!")

@allure.step("Проверить, что коллекция пользователя не изменилась")
def assert_collection_unchanged(user):
    response = user["api"].get_user(user["user_id"])
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["userId"] == user["user_id"]
    assert data["username"] == user["username"]
    assert isinstance(data["books"], list)
    assert sorted(book["isbn"] for book in data["books"]) == sorted(
        book["isbn"] for book in user["books"]
    )

@pytest.mark.parametrize("token", [None, "invalid-token"], ids=["no-token", "invalid-token"])
@allure.title("Список книг профиля защищён авторизацией")
def test_get_profile_requires_token(api_user_with_books, anonymous_api, token):
    if token is not None:
        anonymous_api.set_token(token)
    with allure.step("Запросить профиль без действующего токена"):
        response = anonymous_api.get_user(api_user_with_books["user_id"])
    assert_error(response, 401, "1200", "User not authorized!")
    assert_collection_unchanged(api_user_with_books)

@allure.title("Добавление книги без токена")
def test_add_book_without_token(api_user, anonymous_api):
    isbn = get_first_isbn(anonymous_api)
    user_id = api_user["user_id"]

    response = anonymous_api.add_book(user_id, isbn)

    assert_error(response, 401, "1200", "User not authorized!")

    with allure.step("Проверить, что коллекция осталась пустой"):
        profile = api_user["api"].get_user(user_id)

        assert profile.status_code == 200, profile.text
        assert profile.json()["books"] == [], profile.text


@allure.title("Регистрация со слабым паролем")
def test_create_user_weak_password(api_client):
    response = api_client.create_user(
        f"weak_{uuid.uuid4().hex}",
        "12345",
    )

    assert_error(
        response,
        400,
        "1300",
        "Passwords must have at least one non alphanumeric character, "
        "one digit ('0'-'9'), one uppercase ('A'-'Z'), "
        "one lowercase ('a'-'z'), one special character "
        "and Password must be eight characters or longer.",
    )

@allure.title("Неверный пароль пользователя")
def test_authorize_wrong_password(api_user):
    response = api_user["api"].authorize(
        api_user["username"],
        "IncorrectPassword123!",
    )

    assert_error(response, 404, "1207", "User not found!")

@allure.title("Нельзя добавить несколько книг без токена")
def test_add_multiple_books_requires_token(api_user_with_books, anonymous_api):
    user = api_user_with_books
    with allure.step("Добавить несколько книг без токена авторизации"):
        response = anonymous_api.add_books(
            user["user_id"], [book["isbn"] for book in user["books"]]
        )
    assert_error(response, 401, "1200", "User not authorized!")
    assert_collection_unchanged(user)

@allure.title("Повторное добавление одной книги отклоняется")
def test_duplicate_book_is_rejected(api_user_with_books):
    user = api_user_with_books
    with allure.step("Добавить книгу, которая уже находится в профиле"):
        response = user["api"].add_book(user["user_id"], user["books"][0]["isbn"])
    assert_error(response, 400, "1210", "ISBN already present in the User's Collection!")
    assert_collection_unchanged(user)

import uuid

import pytest
import allure

def get_first_isbn(api):
    response = api.get_books()
    assert response.status_code == 200, response.text
    books = response.json()["books"]
    assert books, "Book Store returned an empty catalog"
    return books[0]["isbn"]

pytestmark = [
    allure.suite("API")
]

@pytest.mark.api
@pytest.mark.positive
@allure.title("API1 - Получение списка всех книг")
def test_get_all_books(api_client):

    response = api_client.get_books()

    assert response.status_code == 200

    books = response.json()["books"]

    assert len(books) > 0

    for book in books:
        assert book["isbn"]
        assert book["title"]
        assert book["author"]



@pytest.mark.api
@pytest.mark.positive
@allure.title("API2 - Получение книги по ISBN")
def test_get_book_by_isbn(api_client):

    books_response = api_client.get_books()

    isbn = books_response.json()["books"][0]["isbn"]

    response = api_client.get_book(isbn)

    assert response.status_code == 200

    book = response.json()

    assert book["isbn"] == isbn
    assert book["title"]
    assert book["author"]

@allure.title("API-NEG-01 - Несуществующий ISBN")
def test_get_book_invalid_isbn(api_client):
    response = api_client.get_book("0000000000000")
    assert response.status_code == 400, response.text
    assert response.json().get("message"), response.text

@pytest.mark.api
@pytest.mark.positive
@allure.title("API3 - Успешная авторизация")
def test_authorized_user(api_user):

    api = api_user["api"]

    response = api.authorize(
        api_user["username"],
        api_user["password"]
    )

    assert response.status_code == 200
    assert response.json() is True

@pytest.mark.api
@pytest.mark.negative
@allure.title("API4 - Ошибка авторизации")
def test_invalid_authorized_user(api_user):

    api = api_user["api"]

    response = api.authorize(
        api_user["username"] + "jjj",
        api_user["password"]
    )

    assert response.status_code == 404

@allure.title("API5 - Неверный пароль пользователя")
def test_authorize_wrong_password(api_user):
    response = api_user["api"].authorize(
        api_user["username"], "IncorrectPassword123!"
    )
    assert response.status_code == 404

@pytest.mark.api
@pytest.mark.positive
@allure.title("API6 - Добавление книги в коллекцию")
def test_add_book(api_user):

    api = api_user["api"]
    user_id = api_user["user_id"]

    books = api.get_books().json()["books"]
    isbn = books[0]["isbn"]

    response = api.add_book(user_id, isbn)

    assert response.status_code == 201

    user_response = api.get_user(user_id)

    assert user_response.status_code == 200

    user_books = user_response.json()["books"]

    assert isbn in [book["isbn"] for book in user_books]



@pytest.mark.api
@pytest.mark.positive
@allure.title("API7 - Удаление книги из коллекции")
def test_delete_book(api_user):

    api = api_user["api"]
    user_id = api_user["user_id"]

    isbn = api.get_books().json()["books"][0]["isbn"]

    add_response = api.add_book(user_id, isbn)

    assert add_response.status_code == 201

    delete_response = api.delete_book(user_id, isbn)

    assert delete_response.status_code == 204

    user_response = api.get_user(user_id)

    user_books = user_response.json()["books"]

    assert isbn not in [
        book["isbn"] for book in user_books
    ]

@allure.title("API8 - Добавление книги без токена")
def test_add_book_without_token(api_user, anonymous_api):
    isbn = get_first_isbn(anonymous_api)
    user_id = api_user["user_id"]

    response = anonymous_api.add_book(user_id, isbn)
    assert response.status_code == 401, response.text

    profile = api_user["api"].get_user(user_id)
    assert profile.status_code == 200, profile.text
    assert isbn not in [book["isbn"] for book in profile.json()["books"]]

@allure.title("API9 - Регистрация со слабым паролем")
def test_create_user_weak_password(api_client):
    response = api_client.create_user(
        f"weak_{uuid.uuid4().hex}", "12345"
    )
    assert response.status_code == 400, response.text
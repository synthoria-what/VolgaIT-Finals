
import uuid

import pytest
import allure

pytestmark = [
    allure.parent_suite("DemoQA Тестирование"),
    allure.suite("API")
]


@allure.step("Проверить HTTP-статус и JSON ошибки")
def assert_error(response, status, code, message):
    assert response.status_code == status, response.text
    assert response.json() == {"code": code, "message": message}, response.text


@pytest.mark.api
@pytest.mark.positive
@allure.title("Получение списка всех книг")
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
@allure.title("Получение книги по ISBN")
def test_get_book_by_isbn(api_client):

    books_response = api_client.get_books()

    isbn = books_response.json()["books"][0]["isbn"]

    response = api_client.get_book(isbn)

    assert response.status_code == 200

    book = response.json()

    assert book["isbn"] == isbn
    assert book["title"]
    assert book["author"]


@pytest.mark.api
@pytest.mark.positive
@allure.title("Успешная авторизация")
def test_authorized_user(api_user):

    api = api_user["api"]

    response = api.authorize(
        api_user["username"],
        api_user["password"]
    )

    assert response.status_code == 200
    assert response.json() is True

@pytest.mark.api
@pytest.mark.positive
@allure.title("Добавление книги в коллекцию")
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
@allure.title("Удаление книги из коллекции")
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

import requests


class BookStoreApi:

    BASE_URL = "https://demoqa.com"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json"
        })

    def get_books(self):
        return self.session.get(
            f"{self.BASE_URL}/BookStore/v1/Books"
        )

    def get_book(self, isbn: str):
        return self.session.get(
            f"{self.BASE_URL}/BookStore/v1/Book",
            params={"ISBN": isbn}
        )

    def create_user(self, username: str, password: str):
        return self.session.post(
            f"{self.BASE_URL}/Account/v1/User",
            json={
                "userName": username,
                "password": password
            }
        )

    def generate_token(self, username: str, password: str):
        return self.session.post(
            f"{self.BASE_URL}/Account/v1/GenerateToken",
            json={
                "userName": username,
                "password": password
            }
        )

    def authorize(self, username: str, password: str):
        return self.session.post(
            f"{self.BASE_URL}/Account/v1/Authorized",
            json={
                "userName": username,
                "password": password
            }
        )

    def set_token(self, token: str):
        self.session.headers.update({
            "Authorization": f"Bearer {token}"
        })

    def add_book(self, user_id: str, isbn: str):
        return self.session.post(
            f"{self.BASE_URL}/BookStore/v1/Books",
            json={
                "userId": user_id,
                "collectionOfIsbns": [
                    {"isbn": isbn}
                ]
            }
        )

    def get_user(self, user_id: str):
        return self.session.get(
            f"{self.BASE_URL}/Account/v1/User/{user_id}"
        )

    def delete_book(self, user_id: str, isbn: str):
        return self.session.delete(
            f"{self.BASE_URL}/BookStore/v1/Book",
            json={
                "userId": user_id,
                "isbn": isbn
            }
        )

    def delete_user(self, user_id: str):
        return self.session.delete(
            f"{self.BASE_URL}/Account/v1/User/{user_id}"
        )

    def close(self):
        self.session.close()

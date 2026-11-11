

from selenium.webdriver.common.by import By


class DemoQABookStoreHelper:
    LOCATOR_SEARCH_FIELD = (By.ID, "searchBox")

    LOCATOR_BOOKS = (
        By.CSS_SELECTOR, ".rt-tbody .rt-tr-group a"
    )


class DemoQABookDetailsHelper:
    LOCATOR_BOOK_TITLE = (
        By.CSS_SELECTOR, "#title-wrapper #userName-value"
    )

    LOCATOR_ADD_BOOK_BUTTON = (By.XPATH, "//button[text()='Add To Your Collection']")


class DemoQAProfileHelper:
    LOCATOR_PROFILE_TABLE = (By.TAG_NAME, "tbody")
    LOCATOR_PROFILE_BOOK = (By.TAG_NAME, "td")
    LOCATOR_PROFILE_BOOK_NAME = (By.TAG_NAME, "a")
    LOCATOR_PROFILE_BOOK_ROWS = (By.TAG_NAME, "tr")

class DemoQALoginHelper:
    LOCATOR_LOGIN_USERNAME_FIELD = (By.ID, "userName")
    LOCATOR_LOGIN_PASSWORD_FIELD = (By.ID, "password")
    LOCATOR_SUBMIT_BUTTON = (By.ID, "login")

    LOCATOR_ERROR_MESSAGE = (By.ID, "name")
    LOCATOR_PROFILE_USERNAME = (By.ID, "userName-value")

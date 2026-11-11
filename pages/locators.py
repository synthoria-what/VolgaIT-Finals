

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

    LOCATOR_ADD_BOOK_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Add To Your Collection']"
    )


class DemoQAProfileHelper:
    LOCATOR_PROFILE_BOOKS = (
        By.CSS_SELECTOR, ".rt-tbody .rt-tr-group a"
    )

class DemoQALoginHelper:
    LOCATOR_DEMOQA_LOGIN_USERNAME_FIELD = (By.ID, "userName")
    LOCATOR_DEMOQA_LOGIN_PASSWORD_FIELD = (By.ID, "password")
    LOCATOR_DEMOQA_SUBMIT_BUTTON = (By.ID, "login")

    LOCATOR_DEMOQA_ERROR_MESSAGE = (By.ID, "name")
    LOCATOR_DEMOQA_PROFILE_USERNAME = (By.ID, "userName-value")
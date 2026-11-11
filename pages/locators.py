

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
    LOCATOR_BOOK_LINKS = (By.CSS_SELECTOR, "tbody a")
    LOCATOR_USERNAME = (By.ID, "userName-value")
    LOCATOR_SEARCH_FIELD = (By.ID, "searchBox")
    LOCATOR_NOT_LOGGED_IN = (By.ID, "notLoggin-label")
    LOCATOR_LOGOUT = (By.XPATH, "//button[normalize-space()='Logout']")
    LOCATOR_GO_TO_STORE = (By.ID, "gotoStore")
    LOCATOR_DELETE_ALL = (By.XPATH, "//button[normalize-space()='Delete All Books']")
    LOCATOR_MODAL = (By.CSS_SELECTOR, ".modal-content")
    LOCATOR_MODAL_TITLE = (By.ID, "example-modal-sizes-title-sm")
    LOCATOR_MODAL_CANCEL = (By.ID, "closeSmallModal-cancel")
    LOCATOR_MODAL_CONFIRM = (By.ID, "closeSmallModal-ok")

class DemoQALoginHelper:
    LOCATOR_LOGIN_USERNAME_FIELD = (By.ID, "userName")
    LOCATOR_LOGIN_PASSWORD_FIELD = (By.ID, "password")
    LOCATOR_SUBMIT_BUTTON = (By.ID, "login")

    LOCATOR_ERROR_MESSAGE = (By.ID, "name")
    LOCATOR_PROFILE_USERNAME = (By.ID, "userName-value")

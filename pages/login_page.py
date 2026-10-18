from pages.core.base_element import BaseElement
from pages.core.button import Button
from pages.core.input import Input
from pages.product_page import ProductPage
from pages.base_page import BasePage


class LoginPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.input_username = Input(page.get_by_placeholder("Username"))
        self.input_password = Input(page.get_by_placeholder("Password"))
        self.btn_login = Button(page.get_by_role("button", name="Login"))
        self.alert_error = BaseElement(page.get_by_role("alert"))

    def submit_credentials(self, username: str, password: str):
        """
        Submit username and password as credentials to login page.

        Args:
            username (str): Username
            password (str): Password
        """
        self.input_username.fill(username)
        self.input_password.fill(password)
        self.btn_login.click()

    def login(self, username: str, password: str) -> ProductPage:
        """
        Calling the submit_credentials method with provided username and password.

        Args:
            username (str): Username
            password (str): Password

        Returns:
            ProductPage: Product page
        """
        self.submit_credentials(username, password)
        return ProductPage(self.page)

    def login_expecting_error(self, username: str, password: str) -> str:
        """
        Calling the submit_credentials method with provided username and password (Wrong Credentials).

        Args:
            username (str): Username
            password (str): Password

        Returns:
            str: Error message
        """
        self.submit_credentials(username, password)
        return self.alert_error.get_text()

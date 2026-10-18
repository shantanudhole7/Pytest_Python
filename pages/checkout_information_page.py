from pages.base_page import BasePage
from pages.checkout_overview_page import CheckoutOverviewPage
from pages.core.base_element import BaseElement
from pages.core.button import Button
from pages.core.input import Input


class CheckoutInformationPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.input_first_name = Input(self.page.get_by_test_id("firstName"))
        self.input_last_name = Input(self.page.get_by_test_id("lastName"))
        self.input_zip_postal_code = Input(self.page.get_by_test_id("postalCode"))
        self.btn_continue = Button(self.page.get_by_test_id("continue"))
        self.alert_error = BaseElement(self.page.get_by_test_id("error"))

    def set_first_name(self, first_name):
        """
        Set the first name of the customer.

        Args:
            first_name (str): The first name of the customer.
        """
        self.input_first_name.fill(first_name)

    def set_last_name(self, last_name):
        """
        Set the last name of the customer.

        Args:
            last_name (str): The last name of the customer.
        """
        self.input_last_name.fill(last_name)

    def set_zip_postal_code(self, zip_postal_code):
        """
        Set the zip or postal code of the customer.

        Args:
            zip_postal_code (str): Zip code of the customer.
        """
        self.input_zip_postal_code.fill(zip_postal_code)

    def set_checkout_information(self, first_name: str, last_name: str, zip_postal_code: str):
        """
        Fill in the checkout information.

        Args:
            first_name (str): The first name of the customer.
            last_name (str): The last name of the customer.
            zip_postal_code (str): The zip or postal code of the customer.
        """
        self.set_first_name(first_name)
        self.set_last_name(last_name)
        self.set_zip_postal_code(zip_postal_code)

    def click_continue(self):
        """
        Click on the continue button.
        """
        self.btn_continue.click()

    def fill_checkout_information_continue(self, first_name: str, last_name: str, zip_postal_code: str) -> CheckoutOverviewPage:
        """
        Fill in the checkout information.

        Args:
            first_name (str): The first name of the customer.
            last_name (str): The last name of the customer.
            zip_postal_code (str): The zip or postal code of the customer.

        Returns:
            CheckoutOverview: The checkout overview.
        """
        self.set_checkout_information(first_name, last_name, zip_postal_code)
        self.click_continue()
        return CheckoutOverviewPage(self.page)

    def get_text_error(self):
        return self.alert_error.get_text()

import pytest
from config.config import APPUSERNAME, PASSWORD
from data.product import CART_PRODUCT_NAMES
from tests.base_test import BaseTest, log_information, assert_text, assert_displayed


class TestE2EScenarioPage(BaseTest):
    FIRST_NAME = "Shantanu"
    LAST_NAME = "Dhole"
    ZIP_POSTAL_CODE = "411057"
    SUCCESS_MESSAGE = "Thank you for your order!"
    FIRST_NAME_ERROR_MESSAGE = "Error: First Name is required"
    LAST_NAME_ERROR_MESSAGE = "Error: Last Name is required"
    ZIP_POSTAL_CODE_ERROR_MESSAGE = "Error: Postal Code is required"

    @pytest.fixture()
    def checkout_information_page(self, login_page):
        """
        Land product page, add products to-checkout click on checkout.

        Args:
            login_page: Login page

        Returns:
            checkout_information_page: Checkout information page
        """
        log_information("Login with Valid username and password")
        _product_page = login_page.login(APPUSERNAME, PASSWORD)

        log_information(f"Add given items to cart: {', '.join(CART_PRODUCT_NAMES)}")
        for _product_name in CART_PRODUCT_NAMES:
            _product_page.click_add_to_cart(_product_name)

        log_information("Click on cart.")
        _cart_page = _product_page.click_on_cart()

        log_information("Land on Checkout Information Page and return.")
        _checkout_information_page = _cart_page.click_checkout()
        return _checkout_information_page

    @pytest.mark.description("E2E Scenario: Verify the complete checkout process from login to order completion.")
    @pytest.mark.ui
    @pytest.mark.e2e
    @pytest.mark.blocker
    def test_complete_checkout_order(self, checkout_information_page):
        """@priority P1 @owner Shantanu @feature checkout_order"""
        log_information("Land on checkout information page and fill the details.")
        _checkout_overview_page = checkout_information_page.fill_checkout_information_continue(self.FIRST_NAME,
                                                                                               self.LAST_NAME,
                                                                                               self.ZIP_POSTAL_CODE)

        log_information("Click on Finish Button.")
        _checkout_complete_page = _checkout_overview_page.click_finish()

        log_information("Assert the text on final checkout.")
        assert_text("Verify that thank you text is displayed", _checkout_complete_page.lbl_complete_header,
                    self.SUCCESS_MESSAGE)
        assert_displayed("Verify that Back Home Button Displayed", _checkout_complete_page.btn_back_home)

    @pytest.mark.description("E2E Scenario: Verify Error messages on Checkout page")
    @pytest.mark.parametrize("_first_name,_last_name, _zip_code, _error_text",
                             [("", LAST_NAME, ZIP_POSTAL_CODE, FIRST_NAME_ERROR_MESSAGE),
                              (FIRST_NAME, "", ZIP_POSTAL_CODE, LAST_NAME_ERROR_MESSAGE),
                              (FIRST_NAME, LAST_NAME, "", ZIP_POSTAL_CODE_ERROR_MESSAGE)],
                             ids=["missing_first_name", "missing_last_name", "missing_zip_code"])
    @pytest.mark.ui
    @pytest.mark.negative
    @pytest.mark.major
    def test_check_out_validation(self, checkout_information_page, _first_name, _last_name, _zip_code, _error_text):
        """@priority P3 @owner Shantanu @feature checkout_validation"""
        log_information("Do not fill one field and click on continue and assert error")
        checkout_information_page.set_checkout_information(_first_name, _last_name, _zip_code)
        checkout_information_page.click_continue()

        log_information("Verify Error message for scenario on keeping field empty")
        assert_text("Verify checkout error when a required field is empty", checkout_information_page.alert_error,
                    _error_text, )
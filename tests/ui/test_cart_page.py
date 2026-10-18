import pytest
from config.config import APPUSERNAME, PASSWORD
from data.product import CART_PRODUCT_NAMES
from tests.base_test import BaseTest, log_information, assert_count


class TestCartPage(BaseTest):

    @pytest.mark.description("Verify the cart item count after adding products.")
    @pytest.mark.ui
    @pytest.mark.major
    def test_verify_cart_count(self, login_page):
        """@priority P3 @owner Shantanu @feature cart"""
        log_information("Login with Valid username and password")
        _product_page = login_page.login(APPUSERNAME, PASSWORD)

        log_information(f"Add given items to cart: {', '.join(CART_PRODUCT_NAMES)}")
        for _product_name in CART_PRODUCT_NAMES:
            _product_page.click_add_to_cart(_product_name)

        log_information("Click on cart.")
        _cart_page = _product_page.click_on_cart()

        log_information("Verify the items in the cart.")
        assert_count("Verify that items count in cart", _cart_page.cart_quantity, len(CART_PRODUCT_NAMES))

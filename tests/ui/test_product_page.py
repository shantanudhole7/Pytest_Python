import pytest
from config.config import APPUSERNAME, PASSWORD
from data.product import PRODUCTS, CART_PRODUCT_NAMES
from tests.base_test import BaseTest, log_information, assert_displayed, assert_equal


class TestProductPage(BaseTest):
    SINGLE_CART_PRODUCT = PRODUCTS["backpack"][0]
    REMOVE_BUTTON_PRODUCT = PRODUCTS["bike_light"][0]
    PRODUCTS_NAMES = [name for name, _ in PRODUCTS.values()]

    @pytest.fixture()
    def product_page(self, login_page):
        log_information("Login with Valid username and password")
        _product_page = login_page.login(APPUSERNAME, PASSWORD)
        return _product_page

    @pytest.mark.description("Verify the price of each product on the product page.")
    @pytest.mark.ui
    @pytest.mark.critical
    @pytest.mark.parametrize(
        "_product_name, _expected_price", PRODUCTS.values(), ids=PRODUCTS.keys()
    )
    def test_verify_price_of_product(self, product_page, _product_name, _expected_price):
        """@priority P2 @owner Shantanu @feature product"""
        log_information(f"Verify the price of the {_product_name} product")
        _actual_product_price = product_page.get_item_price(_product_name)
        assert_equal(f"Verify price of {_product_name}", _expected_price, _actual_product_price)

    @pytest.mark.description("Verify Add to Cart Button for each product on the product page.")
    @pytest.mark.ui
    @pytest.mark.major
    @pytest.mark.parametrize(
        "_product_name", PRODUCTS_NAMES, ids=PRODUCTS.keys())
    def test_verify_add_to_cart_button(self, product_page, _product_name):
        """@priority P3 @owner Shantanu @feature product"""
        log_information(f"Verify the add to cart button for {_product_name}")
        assert_displayed(f"Verify add to cart button for {_product_name}",
                         product_page.get_button_add_to_cart(_product_name))

    @pytest.mark.description("Verify the empty cart on first login.")
    @pytest.mark.ui
    @pytest.mark.trivial
    def test_empty_cart_value(self, product_page):
        """@priority P5 @owner Shantanu @feature product"""
        log_information("Verify the empty cart on login.")
        assert_equal("Verify empty cart login", 0, product_page.get_cart_value())

    @pytest.mark.description("Verify that user can add item to cart.")
    @pytest.mark.ui
    @pytest.mark.minor
    @pytest.mark.parametrize(
        "_product_names",
        [
            [SINGLE_CART_PRODUCT],
            CART_PRODUCT_NAMES,
        ],
        ids=["one_item_in_cart", "two_items_in_cart"]
    )
    def test_verify_cart_value(self, product_page, _product_names):
        """@priority P4 @owner Shantanu @feature product"""
        log_information("Add item to cart.")
        for _product_name in _product_names:
            product_page.click_add_to_cart(_product_name)

        log_information("Verify the items in the cart after adding item to cart.")
        assert_equal("Verify the items in the cart after adding item to cart.", len(_product_names),
                     product_page.get_cart_value())

    @pytest.mark.description("Verify that user able to see remove button after adding item to cart.")
    @pytest.mark.ui
    @pytest.mark.minor
    def test_verify_remove_button(self, product_page):
        """@priority P3 @owner Shantanu @feature product"""
        log_information(f"Add item {self.REMOVE_BUTTON_PRODUCT} to cart.")
        product_page.click_add_to_cart(self.REMOVE_BUTTON_PRODUCT)

        log_information("Verify the remove button after adding item to cart.")
        assert_displayed(f"Verify remove button for {self.REMOVE_BUTTON_PRODUCT}",
                         product_page.get_button_remove(self.REMOVE_BUTTON_PRODUCT))

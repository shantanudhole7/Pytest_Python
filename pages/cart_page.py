from pages.base_page import BasePage
from pages.checkout_information_page import CheckoutInformationPage
from pages.core.base_element import BaseElement
from pages.core.button import Button


class CartPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.cart_quantity = BaseElement(page.get_by_test_id("cart-list").get_by_test_id("inventory-item"))
        self.btn_checkout = Button(page.get_by_test_id("checkout"))

    def get_cart_quantity(self):
        """
        Get items quantity in the cart.

        Returns:
             Items quantity in the cart.
        """
        self.cart_quantity.locator.first.wait_for(state="visible")
        return self.cart_quantity.get_count()

    def click_checkout(self) -> CheckoutInformationPage:
        """
        Click on the checkout button.

        Returns:
            CheckoutPage: The checkout page object.
        """
        self.btn_checkout.click()
        return CheckoutInformationPage(self.page)

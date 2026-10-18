from pages.base_page import BasePage
from pages.checkout_complete_page import CheckoutCompletePage
from pages.core.base_element import BaseElement
from pages.core.button import Button
from pages.core.label import Label


class CheckoutOverviewPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.lbl_cart_quantity = BaseElement(page.get_by_test_id("cart-list").get_by_test_id("inventory-item"))
        self.lbl_payment_information = Label(page.get_by_test_id("payment-info-label"))
        self.lbl_subtotal = Label(page.get_by_test_id("subtotal-label"))
        self.btn_finish = Button(page.get_by_test_id("finish"))


    def click_finish(self) -> CheckoutCompletePage:
        self.btn_finish.click()
        return CheckoutCompletePage(self.page)

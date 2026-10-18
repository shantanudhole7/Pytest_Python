from pages.base_page import BasePage
from pages.core.button import Button
from pages.core.label import Label


class CheckoutCompletePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.lbl_complete_header = Label(page.get_by_test_id("complete-header"))
        self.btn_back_home = Button(page.get_by_test_id("back-to-products"))
        self.btn_generate_pdf = Button(page.get_by_test_id("generate-pdf-order"))

    def get_text_complete_header(self) -> str:
        """
        Get the text of the complete header.

        Returns:
            str: The text of the complete header.
        """
        return self.lbl_complete_header.get_text()

    def is_display_back_home(self) -> bool:
        """
        Check if the back home page is displayed.

        Returns:
            bool: True if the back home page is displayed, False otherwise.
        """
        return self.btn_back_home.is_displayed()

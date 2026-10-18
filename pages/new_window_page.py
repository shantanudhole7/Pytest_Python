from pages.base_page import BasePage
from pages.core.label import Label


class NewWindowPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.lbl_heading = Label(self.page.locator(".entry-content .wp-block-heading").first)

    def get_lbl_heading(self):
        """
        Heading on the opened page with the given text.
        """
        return self.lbl_heading.get_text()

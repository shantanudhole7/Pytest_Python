from pages.base_page import BasePage
from pages.core.button import Button
from pages.core.label import Label
from pages.new_window_page import NewWindowPage


class WindowPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.btn_new_tab = Button(self.page.get_by_role("button", name="New Tab"))
        self.btn_new_window = Button(self.page.get_by_role("button", name="New Window"))
        self.lbl_new_tab_message = Label(self.page.locator(".entry-content"))

    def click_new_tab(self) -> NewWindowPage:
        """click on the new tab button

        Returns:
            New window as a Playwright Page.
        """
        with self.page.expect_popup() as new_tab_info:
            self.btn_new_tab.click()

        return NewWindowPage(new_tab_info.value)

    def click_new_window(self) -> NewWindowPage:
        """click on the new window button

        Returns:
            New window as a Playwright Page.
        """
        with self.page.expect_popup() as new_window_info:
            self.btn_new_window.click()

        return NewWindowPage(new_window_info.value)

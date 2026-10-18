from pages.base_page import BasePage
from pages.core.button import Button
from pages.core.dialog import Dialog
from pages.core.label import Label


class AlertPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.btn_alert_popup = Button(self.page.get_by_role("button", name="Alert Popup"))
        self.btn_confirm_popup = Button(self.page.get_by_role("button", name="Confirm Popup"))
        self.btn_prompt_popup = Button(self.page.get_by_role("button", name="Prompt Popup"))
        self.lbl_confirm_popup_message = Label(self.page.locator("#confirmResult"))
        self.lbl_prompt_popup_message = Label(self.page.locator("#promptResult"))
        self.dialog = Dialog(page)

    def click_alert_popup(self):
        """
        Click the alert popup button.
        """
        self.btn_alert_popup.click()

    def click_confirm_popup(self):
        """
        Click the confirm popup button.
        """
        self.btn_confirm_popup.click()

    def click_prompt_popup(self):
        """
        Click the prompt popup button.
        """
        self.btn_prompt_popup.click()

    def get_alert_popup_message(self) -> str:
        """
        Click the alert popup button and return the dialog message.

        Returns:
            str: The alert popup message.
        """
        self.dialog.accept_next()
        self.click_alert_popup()
        return self.dialog.message

    def get_confirm_popup_message(self, _is_accept) -> str:
        """
        Get the confirmation popup message.

        Args:
            _is_accept (bool): Whether the popup is accepted or not.

        Returns:
            str: The confirmation popup message.
        """
        if _is_accept:
            self.dialog.accept_next()
        else:
            self.dialog.dismiss_next()
        self.click_confirm_popup()
        return self.dialog.message

    def get_confirm_popup_accepted_message(self) -> str:
        """
        Get the confirmation popup accepted message.

        Returns:
            str: The confirmation popup message.
        """
        return self.lbl_confirm_popup_message.get_text()

    def get_prompt_popup_message(self, _name) -> str:
        """
        Get the prompt popup message.

        Args:
            _name (str): Enter the name and accept the popup message.

        Returns:
            str: The prompt popup message.
        """
        self.dialog.accept_next(_name)
        self.click_prompt_popup()
        return self.dialog.message

    def get_prompt_popup_accepted_message(self) -> str:
        """
        Get the prompt popup accepted message.

        Returns:
            str: The prompt popup message.
        """
        return self.lbl_prompt_popup_message.get_text()

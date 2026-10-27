from pages.base_page import BasePage
from pages.core.checkbox import Checkbox
from pages.core.radio import Radio


class PracticePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.rdo_radio_1 = Radio(page.locator("input[type='radio'][value='radio1']"))
        self.rdo_radio_2 = Radio(page.locator("input[type='radio'][value='radio2']"))
        self.rdo_radio_3 = Radio(page.locator("input[type='radio'][value='radio3']"))
        self.chk_checkbox_1 = Checkbox(page.locator("#checkBoxOption1"))
        self.chk_checkbox_2 = Checkbox(page.locator("#checkBoxOption2"))
        self.chk_checkbox_3 = Checkbox(page.locator("#checkBoxOption3"))

    # noinspection PyMethodMayBeStatic
    def check_radio(self, radio: Radio) -> None:
        """
        Check the given radio button.

        Args:
           radio (Radio): The radio button to check, e.g. self.rdo_radio_1.
        """
        radio.check()

    # noinspection PyMethodMayBeStatic
    def is_checked(self, radio: Radio) -> bool:
        """
        Check the given radio button is checked.

        Args:
            radio (Radio): The radio button to check, e.g. self.rdo_radio_1.
        Returns:
            bool: True if the radio button is checked, False otherwise.
        """
        return radio.is_checked()

    # noinspection PyMethodMayBeStatic
    def check_checkbox(self, checkbox: Checkbox) -> None:
        """
        Check the given checkbox.

        Args:
           checkbox (Checkbox): The Checkbox button to check, e.g. self.chk_checkbox_1.
        """
        checkbox.check()

    # noinspection PyMethodMayBeStatic
    def uncheck_checkbox(self, checkbox: Checkbox) -> None:
        """
        Un-check the given checkbox.

        Args:
           checkbox (Checkbox): The Checkbox button to check, e.g. self.chk_checkbox_1.
        """
        checkbox.uncheck()
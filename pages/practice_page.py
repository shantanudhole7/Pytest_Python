from pages.base_page import BasePage
from pages.core.radio import Radio


class PracticePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.chk_radio_1 = Radio(page.locator("input[type='radio'][value='radio1']"))
        self.chk_radio_2 = Radio(page.locator("input[type='radio'][value='radio2']"))
        self.chk_radio_3 = Radio(page.locator("input[type='radio'][value='radio3']"))

    # noinspection PyMethodMayBeStatic
    def check_radio(self, radio: Radio) -> None:
        """
           Check the given radio button.

           Args:
               radio (Radio): The radio button to check, e.g. self.chk_radio_1.
           """
        radio.check()

    # noinspection PyMethodMayBeStatic
    def is_checked(self, radio: Radio) -> bool:
        """
        Check the given radio button is checked.

        Args:
            radio (Radio): The radio button to check, e.g. self.chk_radio_1.
        Returns:
            bool: True if the radio button is checked, False otherwise.
        """
        return radio.is_checked()

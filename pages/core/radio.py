from playwright.sync_api import Locator
from pages.core.base_element import BaseElement

class Radio(BaseElement):
    def __init__(self, locator: Locator):
        super().__init__(locator)
        self.locator = locator

    def check(self):
        """
        Check the radio element.
        """
        self.locator.check()

    def is_checked(self) -> bool:
        """
        Verify the element checked.

        Returns:
            bool: True if checked, False otherwise.
        """
        return super().is_checked()

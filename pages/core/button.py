from playwright.sync_api import Locator
from pages.core.base_element import BaseElement


class Button(BaseElement):
    def __init__(self, locator: Locator):
        super().__init__(locator)
        self.locator = locator

    def click(self):
        """
        Click the button element.
        """
        super().click()

    def double_click(self):
        """
        Double-click the button element.
        """
        self.locator.dblclick()

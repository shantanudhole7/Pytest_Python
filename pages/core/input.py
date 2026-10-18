from playwright.sync_api import Locator
from pages.core.base_element import BaseElement


class Input(BaseElement):
    def __init__(self, locator: Locator):
        super().__init__(locator)

    def fill(self, value: str):
        """
        Clear the input and type the given value.

        Args:
            value: Text to enter into the input.
        """
        self.locator.fill(value)

    def clear(self):
        """
        Remove all text from the input.
        """
        self.locator.clear()

    def get_value(self) -> str:
        """
        Return the current value of the input.

        Returns:
            The text currently in the input, or an empty string if it is empty.
        """
        return self.locator.input_value()

    def select_text(self):
        """
        Select all text in the input.
        """
        self.locator.select_text()

    def is_editable(self) -> bool:
        """
        Return whether the input can be edited.

        Returns:
            True if the input is enabled and not read-only, otherwise False.
        """
        return self.locator.is_editable()

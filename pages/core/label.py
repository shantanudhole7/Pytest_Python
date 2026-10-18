from pages.core.base_element import BaseElement


class Label(BaseElement):
    def __init__(self, locator):
        super().__init__(locator)

    def get_label_text(self) -> str:
        """
        Get the text of the label.

        Returns:
            str: The text of the label.
        """
        return self.locator.text_content()
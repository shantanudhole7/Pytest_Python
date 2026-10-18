from playwright.sync_api import Locator, TimeoutError as PlaywrightTimeoutError, Frame


class BaseElement:
    """Actions common to every element type. Type-specific actions live in subclasses."""

    def     __init__(self, locator: Locator):
        self.locator = locator

    # -------------------------
    # State
    # -------------------------

    def is_visible(self) -> bool:
        """
        Wait up to `timeout` ms for the element to become visible.

        Returns:
            bool: True if the element is visible, False otherwise.
        """
        return self.locator.is_visible()

    def is_hidden(self) -> bool:
        """
        Wait up to `timeout` ms for the element to become hidden.

        Returns:
            bool: True if the element is hidden, False otherwise.
        """
        return self.locator.is_hidden()

    def is_enabled(self) -> bool:
        """
        Wait up to `timeout` ms for the element to become enabled.

        Returns:
            bool: True if the element is enabled, False otherwise.
        """
        return self.locator.is_enabled()

    def is_disabled(self) -> bool:
        """
        Wait up to `timeout` ms for the element to become disabled.

        Returns:
            bool: True if the element is disabled, False otherwise.
        """
        return self.locator.is_disabled()

    def is_displayed(self, timeout: int = 5000) -> bool:
        """
        Wait up to `timeout` ms for the element to become displayed.

        Args:
            timeout (int): Timeout in ms for the element to become displayed.

        Returns:
            bool: True if the element is displayed, False otherwise.
        """
        try:
            self.locator.wait_for(state="visible", timeout=timeout)
            return True
        except PlaywrightTimeoutError:
            return False

    # -------------------------
    # Information
    # -------------------------

    def get_attribute(self, name: str) -> str | None:
        """
        Get the value of an attribute.

        Args:
            name (str): The name of the attribute to get.

        Returns:
            str | None: The value of the attribute or None if it doesn't exist.
        """
        return self.locator.get_attribute(name)

    def get_text(self) -> str:
        """
        Get the text content of the element.

        Returns:
            str: The text content of the element.
        """
        return self.locator.inner_text()

    def get_text_content(self) -> str | None:
        """
        Get the text content of the element.

        Returns:
            str | None: The text content of the element or None if it doesn't exist.
        """
        return self.locator.text_content()

    def get_count(self) -> int:
        """
        Get the number of elements in the page.

        Returns:
            int: The number of elements in the page.
        """
        return self.locator.count()

    # -------------------------
    # Common actions
    # -------------------------

    def focus(self):
        """
        Focus the element on the screen.
        """
        self.locator.focus()

    def blur(self):
        """
        Blur the element.
        """
        self.locator.blur()

    def press(self, key: str):
        """
        Press the given key in the element.

        Args:
            key (str): The key to press.
        """
        self.locator.press(key)

    def screenshot(self, path: str):
        """
        Take a screenshot of the element.

        Args:
            path (str): The path to save the screenshot.
        """
        self.locator.screenshot(path=path)

    def click(self):
        """
        Click the button element.
        """
        self.locator.click()

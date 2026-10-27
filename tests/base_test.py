from playwright.sync_api import expect
from fixtures.logging_fixture import logger
from pages.core.base_element import BaseElement
from pages.core.radio import Radio
from utils.Assertions.assertion import Assertion


def log_information(description: str):
    """
    Log a numbered test step, e.g. 'Login with valid credentials.'

    Args:
        description (str): The description of the test step.
    """
    BaseTest().log_information(description=description)


def assert_equal(description, expected, actual):
    """
    Call assert_equal method of BaseTest class
    """
    BaseTest().assert_equal(description=description, expected=expected, actual=actual)


def assert_displayed(description, element):
    """
    Call assert_equal method of BaseTest class
    """
    BaseTest().assert_displayed(description=description, element=element)


def assert_text(description: str, element, expected: str, timeout: int = 10000):
    """
    Call assert_text method of BaseTest class
    """
    BaseTest().assert_text(description=description, element=element, expected=expected, timeout=timeout)


def assert_http_ok(description: str, response):
    """
    Call assert_http_ok method of BaseTest class
    """
    BaseTest().assert_http_ok(description=description, response=response)


def assert_url(description: str, page, expected_url: str):
    """
    Call assert_url method of BaseTest class
    """
    BaseTest().assert_url(description=description, page=page, expected_url=expected_url)


def assert_count(description: str, element, expected: int, timeout: int = 10000):
    """
    Call assert_count method of BaseTest class
    """
    BaseTest().assert_count(description=description, element=element, expected=expected, timeout=timeout)


def assert_checked(description: str, element):
    """
    Call assert_checked method of BaseTest class
    """
    BaseTest().assert_checked(description=description, element=element)

def assert_unchecked(description: str, element):
    """
    Call assert_unchecked method of BaseTest class
    """
    BaseTest().assert_unchecked(description=description, element=element)


class BaseTest(Assertion):

    @staticmethod
    def log_information(description: str):
        """
        Log a numbered test step, e.g. 'Login with valid credentials.'

        Args:
            description (str): The description of the test step.
        """
        logger.info(description)

    def assert_equal(self, description, expected, actual):
        """
        Assert that two elements are equal.

        Args:
            description (str): The description of the assertion.
            expected: The expected value.
            actual: The actual value.

        """
        self.assert_equal_logger(description, expected, actual)

    def assert_displayed(self, description, element):
        """
        Assert that an element becomes visible, waiting up to `timeout` ms.

        Logs a PASS line through assert_equal when the element is visible,
        or a FAIL line before re-raising when it is not.

        Args:
            description: What is being verified, e.g. "Verify add to cart button is displayed."
            element: Core element (Button, Label, Input, ...) whose visibility is checked.

        Raises:
            AssertionError: If the element is not visible within `timeout`.
        """
        try:
            expect(element.locator).to_be_visible(timeout=10000)
        except AssertionError as e:
            Assertion.logger_error(description, "visible", "not visible")
            raise e
        self.assert_equal(description, True, element.is_displayed())

    def assert_text(self, description: str, element, expected: str, timeout: int = 10000):
        """
        Assert that an element's text equals `expected`, retrying until it matches or `timeout` ms pass.

        Args:
            description: What is being verified.
            element: Core element (Label, Button, ...) whose text is checked.
            expected: Expected text.
            timeout: Maximum time to wait for the text to match, in milliseconds.

        Raises:
            AssertionError: If the text does not match within `timeout`.
        """
        try:
            expect(element.locator).to_have_text(expected, timeout=timeout)
        except AssertionError:
            Assertion.logger_error(description, expected, element.get_text())
            raise
        self.assert_equal(description, expected, element.get_text())

    def assert_http_ok(self, description: str, response):
        """
        Assert that an HTTP response has a status text of OK.

        Args:
            description: What is being verified.
            response: Response object.
        """
        _allowed = ["OK", "Created"]
        if response.status_text not in _allowed:
            Assertion.logger_error(description, " or ".join(_allowed),
                                   f"{response.status_text} | Body: {response.text()}")
        self.assert_equal(description, True, response.status_text in _allowed)

    def assert_url(self, description: str, page, expected_url: str, timeout: int = 10000):
        """
        Assert that the url is equal to expected_url

        Args:
            description: The description of the assertion.
            page: The page object.
            expected_url: The expected url.
            timeout: The timeout in seconds.

        Raises:
            AssertionError: If the element is not visible within `timeout`.
        """
        try:
            expect(page).to_have_url(expected_url, timeout=timeout)
        except AssertionError:
            Assertion.logger_error(description, expected_url, page.url)
            raise
        self.assert_equal(description, expected_url, page.url)

    def assert_count(self, description: str, element, expected: int, timeout: int = 10000):
        """
        Assert that a locator matches exactly `expected` elements, retrying until it does or `timeout` ms pass.

        Args:
            description: What is being verified, e.g. "Verify two items are in the cart."
            element: Core element (BaseElement, Button, Label, ...) whose locator matches the items to count.
            expected: Expected number of matching elements.
            timeout: Maximum time to wait for the count to match, in milliseconds.

        Raises:
            AssertionError: If the count does not match within `timeout`.
        """
        try:
            expect(element.locator).to_have_count(expected, timeout=timeout)
        except AssertionError:
            Assertion.logger_error(description, expected, element.locator.count())
            raise
        self.assert_equal(description, expected, element.get_count())

    def assert_checked(self, description, element):
        """
        Assert that a checkbox or radio button becomes checked, waiting up to 10 seconds.

        Logs a PASS line through assert_equal when the element is checked,
        or a FAIL line before re-raising when it is not.

        Args:
            description: What is being verified, e.g. "Verify chk_radio_1 is checked."
            element: Core element (Checkbox, Radio...) whose checked state is verified.

        Raises:
            AssertionError: If the element is not checked within 10 seconds.
        """
        try:
            expect(element.locator).to_be_checked(timeout=10000)
        except AssertionError as e:
            Assertion.logger_error(description, "checked", "not checked")
            raise e
        self.assert_equal(description, True, BaseElement(element).is_checked())

    def assert_unchecked(self, description, element):
        """
        Assert that a checkbox or radio button becomes un-checked, waiting up to 10 seconds.

        Logs a PASS line through assert_equal when the element is un-checked,
        or a FAIL line before re-raising when it is not.

        Args:
            description: What is being verified, e.g. "Verify chk_radio_1 is checked."
            element: Core element (Checkbox, Radio...) whose un-checked state is verified.

        Raises:
            AssertionError: If the element is not un-checked within 10 seconds.
        """
        try:
            expect(element.locator).not_to_be_checked(timeout=10000)
        except AssertionError as e:
            Assertion.logger_error(description, "un-checked", "checked")
            raise e
        self.assert_equal(description, False, BaseElement(element).is_checked())
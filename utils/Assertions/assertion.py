from fixtures.logging_fixture import logger


class Assertion:

    @staticmethod
    def logger_info(description: str, expected, actual):
        """
        Log a passed check in the standard PASS format.

        Args:
            description (str): What was verified.
            expected: The expected value.
            actual: The actual value.
        """
        logger.info(f"PASS | {description} | Expected: {expected} | Actual: {actual}")

    @staticmethod
    def logger_error(description: str, expected, actual):
        """
        Log a failed check in the standard FAIL format.

        Args:
            description (str): What was verified.
            expected: The expected value.
            actual: The actual value.
        """
        logger.error(f"FAIL | {description} | Expected: {expected} | Actual: {actual}")

    @staticmethod
    def assert_equal_logger(description: str, expected, actual):
        """
        Assert that two objects are equal

        Args:
            description (str): The description of the assertion.
            expected: The expected value.
            actual: The actual value.
        """
        if expected == actual:
            Assertion.logger_info(description, expected, actual)
        else:
            Assertion.logger_error(description, expected, actual)

        assert expected == actual, f"{description} | "f"Expected: {expected} | "f"Actual: {actual}"


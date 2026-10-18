import pytest
from config.config import PRACTICEURL, POPUPSPATH
from pages.alert_page import AlertPage
from tests.base_test import BaseTest, log_information, assert_equal, assert_text


class TestAlertPage(BaseTest):
    PROMPT_NAME = 'Shantanu'
    ALERT_MESSAGE = 'Hi there, pal!'
    CONFIRM_MESSAGE = "OK or Cancel, which will it be?"
    CONFIRM_MESSAGE_OK = 'OK it is!'
    CONFIRM_MESSAGE_CANCEL = 'Cancel it is!'
    PROMPT_MESSAGE = "Hi there, what's your name?"
    PROMPT_MESSAGE_NAME = 'Nice to meet you, {name}!'
    PROMPT_MESSAGE_EMPTY = 'Fine, be that way...'

    @pytest.fixture
    def url(self):
        return f"{PRACTICEURL}{POPUPSPATH}"

    @pytest.mark.description("Verify the alert message is displayed correctly.")
    @pytest.mark.ui
    @pytest.mark.dialog
    def test_verify_alert_message(self, navigate_url):
        """@priority P2 @owner Shantanu @feature alert"""
        log_information("Navigate to the alert page")
        _alert_page = AlertPage(navigate_url)

        log_information("Click on the alert popup button")
        _alert_message = _alert_page.get_alert_popup_message()

        log_information("Verify the alert message.")
        assert_equal("Verify the alert message.", self.ALERT_MESSAGE, _alert_message)

    @pytest.mark.description("Verify the confirm message is displayed correctly.")
    @pytest.mark.ui
    @pytest.mark.dialog
    @pytest.mark.parametrize(
        "_is_accept, _expected_message",
        [
            (True, CONFIRM_MESSAGE_OK),
            (False, CONFIRM_MESSAGE_CANCEL),
        ],
        ids=["accept_confirm", "dismiss_confirm"],
    )
    def test_verify_confirm_message(self, navigate_url, _is_accept, _expected_message):
        """@priority P2 @owner Shantanu @feature alert"""
        log_information("Navigate to the alert page")
        _alert_page = AlertPage(navigate_url)

        log_information("Click on the confirm popup button")
        _confirm_message = _alert_page.get_confirm_popup_message(_is_accept)

        log_information("Verify the confirm dialog text.")
        assert_equal("Verify the confirm dialog text.", self.CONFIRM_MESSAGE, _confirm_message)

        log_information("Verify message is displayed correctly as per click.")
        assert_text("Verify the confirm result message.", _alert_page.lbl_confirm_popup_message, _expected_message)

    @pytest.mark.description("Verify the prompt message is displayed correctly.")
    @pytest.mark.ui
    @pytest.mark.dialog
    @pytest.mark.major
    @pytest.mark.parametrize(
        "_name, _expected_message",
        [
            (PROMPT_NAME, PROMPT_MESSAGE_NAME.format(name=PROMPT_NAME)),
            ("", PROMPT_MESSAGE_EMPTY)
        ],
        ids=["with_name", "without_name"],
    )
    def test_verify_prompt_message(self, navigate_url, _name, _expected_message):
        """@priority P3 @owner Shantanu @feature alert"""
        log_information("Navigate to the alert page")
        _alert_page = AlertPage(navigate_url)

        log_information("Click on the prompt popup button")
        _prompt_message = _alert_page.get_prompt_popup_message(_name)

        log_information("Verify the prompt dialog text.")
        assert_equal("Verify the prompt dialog text.", self.PROMPT_MESSAGE, _prompt_message)

        log_information("Verify message is displayed correctly as per click.")
        assert_text("Verify the prompt result message.", _alert_page.lbl_prompt_popup_message, _expected_message)

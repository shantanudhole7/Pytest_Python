import pytest
from config.config import PRACTICEURL, WINDOWOPERATIONSPATH
from pages.window_page import WindowPage
from tests.base_test import BaseTest, log_information, assert_text


class TestWindowPage(BaseTest):
    NEW_TAB_WINDOW_HEADING = "Start learning"

    @pytest.fixture
    def url(self):
        return f"{PRACTICEURL}{WINDOWOPERATIONSPATH}"

    @pytest.mark.description(
        "Verify the new tab opened after click on new tab button and heading is displayed correctly.")
    @pytest.mark.ui
    @pytest.mark.windows
    @pytest.mark.trivial
    def test_new_tab_page(self, navigate_url):
        """@priority P5 @owner Shantanu @feature window"""
        log_information("Navigate to the windows page url")
        _window_page = WindowPage(navigate_url)

        log_information("Click on the new tab button")
        _new_tab_page = _window_page.click_new_tab()

        log_information("Assert the new tab heading is displayed correctly.")
        assert_text("Verify new tab heading.", _new_tab_page.lbl_heading, self.NEW_TAB_WINDOW_HEADING)

    @pytest.mark.description(
        "Verify the new window opened after click on new window button and heading is displayed correctly.")
    @pytest.mark.ui
    @pytest.mark.windows
    @pytest.mark.trivial
    def test_new_window_page(self, navigate_url):
        """@priority P5 @owner Shantanu @feature window"""
        log_information("Navigate to the window page")
        _window_page = WindowPage(navigate_url)

        log_information("Click on the new window button")
        _new_window_page = _window_page.click_new_window()

        log_information("Assert the new window heading is displayed correctly.")
        assert_text("Verify new window heading.", _new_window_page.lbl_heading, self.NEW_TAB_WINDOW_HEADING)

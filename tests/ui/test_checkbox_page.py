import pytest
from config.config import WEBFORMURL
from pages.practice_page import PracticePage
from tests.base_test import BaseTest, log_information, assert_checked, assert_unchecked


class TestCheckboxPage(BaseTest):

    @pytest.fixture
    def url(self):
        return WEBFORMURL

    @pytest.fixture
    def practice_page(self, navigate_url) -> PracticePage:
        """
        Open WEBFORMURL and return it as a PracticePage.

        Args:
            navigate_url: The shared tab, already on WEBFORMURL.

        Returns:
            PracticePage: The practice page object.
        """
        return PracticePage(navigate_url)

    @pytest.mark.description("Verify a checkbox can be checked and un-checked.")
    @pytest.mark.ui
    @pytest.mark.minor
    def test_checkbox_check_and_uncheck(self, practice_page):
        """@priority P4 @owner Shantanu @feature checkbox"""
        log_information("Check first checkbox")
        practice_page.check_checkbox(practice_page.chk_checkbox_1)

        log_information("Verify that first checkbox is checked")
        assert_checked("Verify that First checkbox is checked", practice_page.chk_checkbox_1)

        log_information("Un-Check first checkbox")
        practice_page.uncheck_checkbox(practice_page.chk_checkbox_1)

        log_information("Verify that first checkbox is un-checked")
        assert_unchecked("Verify that First checkbox is un-checked", practice_page.chk_checkbox_1)

    @pytest.mark.description("Verify several checkboxes can be checked and un-checked independently.")
    @pytest.mark.ui
    @pytest.mark.minor
    def test_multiple_checkboxes_toggle(self, practice_page):
        """@priority P4 @owner Shantanu @feature checkbox"""
        log_information("Check the first and second checkbox.")
        practice_page.check_checkbox(practice_page.chk_checkbox_1)
        practice_page.check_checkbox(practice_page.chk_checkbox_2)

        log_information("Verify that first and second checkbox is checked")
        assert_checked("Verify that First checkbox is checked", practice_page.chk_checkbox_1)
        assert_checked("Verify that Second checkbox is checked", practice_page.chk_checkbox_2)

        log_information("Un-check the second checkbox and check the third checkbox")
        practice_page.uncheck_checkbox(practice_page.chk_checkbox_2)
        practice_page.check_checkbox(practice_page.chk_checkbox_3)

        log_information("Verify second checkbox un-check and third checkbox is checked")
        assert_unchecked("Verify that Second checkbox is un-checked", practice_page.chk_checkbox_2)
        assert_checked("Verify that Third checkbox is checked", practice_page.chk_checkbox_3)

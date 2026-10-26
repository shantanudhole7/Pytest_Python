import pytest
from config.config import WEBFORMURL
from pages.practice_page import PracticePage
from tests.base_test import BaseTest, log_information, assert_checked


class TestRadioPage(BaseTest):

    @pytest.fixture
    def url(self):
        return WEBFORMURL

    @pytest.mark.description("Verify each radio button can be selected.")
    @pytest.mark.ui
    @pytest.mark.minor
    @pytest.mark.parametrize("_radio_name", ["rdo_radio_1", "rdo_radio_2", "rdo_radio_3"])
    def test_radio_button_checked(self, navigate_url, _radio_name):
        """@priority P4 @owner Shantanu @feature form"""
        log_information("Open the practice page")
        _practice_page = PracticePage(navigate_url)
        _radio = getattr(_practice_page, _radio_name)

        log_information(f"Check {_radio_name}")
        _practice_page.check_radio(_radio)

        log_information(f"Verify that {_radio_name} is checked")
        assert_checked(f"Verify that {_radio_name} is checked", _radio)

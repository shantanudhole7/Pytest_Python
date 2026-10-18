import pytest
from config.config import PRACTICEURL, IFRAMEPATH
from pages.frame_page import FramePage
from tests.base_test import BaseTest, log_information, assert_text


class TestFramePage(BaseTest):
    FRAME_1_DOCS_HEADER = "Installation"
    FRAME_2_DOCS_HEADER = "The Selenium Browser Automation Project"

    @pytest.fixture
    def url(self):
        return f"{PRACTICEURL}{IFRAMEPATH}"

    @pytest.mark.description("Verify the header of the docs page inside the frame.")
    @pytest.mark.parametrize("_frame_name, _expected_header",
                             [
                                 ("frame_1", FRAME_1_DOCS_HEADER),
                                 ("frame_2", FRAME_2_DOCS_HEADER)
                             ],
                             ids=["iframe_1", "iframe_2"])
    @pytest.mark.ui
    @pytest.mark.minor
    def test_docs_header_inside_frame(self, navigate_url, _frame_name, _expected_header):
        """@priority P4 @owner Shantanu @feature frame"""
        log_information("Navigate to the frame page url")
        _frame_page = FramePage(navigate_url, _frame_name)

        log_information("Click on the docs button")
        _frame_page.click_on_docs()

        log_information("Assert the header of the docs page")
        assert_text("Verify the header of the docs page", _frame_page.lbl_page_header, _expected_header)

import pytest
from config.config import APPUSERNAME, PASSWORD, HOMEPAGEHEADING, BASEURL, LOCKEDUSERERROR, LOGINERROR, WRONGPASSWORD, \
    LOCKEDUSERNAME, INVENTORYPATH
from tests.base_test import BaseTest, log_information, assert_url, assert_text


class TestLoginPage(BaseTest):

    @pytest.mark.description("Verify a valid user lands on the home page after logging in.")
    @pytest.mark.ui
    @pytest.mark.blocker
    def test_valid_user_login(self, login_page):
        """@priority P1 @owner Shantanu @feature login"""
        log_information("Login with Valid username and password")
        _product_page = login_page.login(APPUSERNAME, PASSWORD)

        log_information("Verify the user able to log in")
        assert_text("Verify home page heading.", _product_page.lbl_page_heading, HOMEPAGEHEADING)
        assert_url("Verify home page URL.", _product_page.page, f"{BASEURL}{INVENTORYPATH}")

    @pytest.mark.description("Verify the correct error message is shown when login fails.")
    @pytest.mark.ui
    @pytest.mark.negative
    @pytest.mark.major
    @pytest.mark.parametrize(
        "_username, _password, _expected_error",
        [
            (LOCKEDUSERNAME, PASSWORD, LOCKEDUSERERROR),
            (APPUSERNAME, WRONGPASSWORD, LOGINERROR),
        ],
        ids=["locked_user", "wrong_password"],
    )
    def test_login_shows_error(self, login_page, _username, _password, _expected_error):
        """@priority P3 @owner Shantanu @feature login"""
        log_information("Login with given username and password for test ids")
        login_page.submit_credentials(_username, _password)

        log_information("Verify the user see corresponding error message")
        assert_text("Verify login error message.", login_page.alert_error, _expected_error)

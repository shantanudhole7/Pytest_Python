import pytest
from config.config import BASEURL, PRACTICEURL
from pages.login_page import LoginPage


@pytest.fixture
def login_page(init_page):
    """
    Open a new page on the login screen and return its LoginPage object.

    Args:
        init_page (new_page): Playwright page object.

    Returns:
        LoginPage: The LoginPage object.
    """
    _login_page = LoginPage(init_page)
    _login_page.navigate(BASEURL)
    yield _login_page


@pytest.fixture
def url():
    """
    Default URL for navigate_url. Override it per test or per class.
    """
    return PRACTICEURL


@pytest.fixture
def navigate_url(init_page, url):
    """
    Navigate to the url specified in init_page. Override it per test.

    Args:
        init_page (new_page): Playwright page object.
        url: URL to navigate to.

    Returns:
        Page: The navigate_url object.
    """
    init_page.goto(url, wait_until="domcontentloaded")
    yield init_page

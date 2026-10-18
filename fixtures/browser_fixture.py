import pytest
from playwright.sync_api import Playwright, BrowserContext, Page
from config.config import HEADLESS, SLOWMO
from fixtures.logging_fixture import attach_page_listeners


def pytest_addoption(parser):
    parser.addoption("--web-browser", action="store", default="chromium", choices=["chromium", "firefox", "webkit"])


@pytest.fixture(scope="module")
def init_context(playwright: Playwright, request):
    """
    One browser context shared by every test in the file.

    Args:
        playwright: Browser shared by every test in the file.
        request: pytest request object.

    Returns:
        context: Browser context with args
    """
    playwright.selectors.set_test_id_attribute("data-test")
    _browser_name = request.config.getoption("--web-browser")
    _args = ["--start-maximized", "--disable-notifications"] if _browser_name == "chromium" else []
    _browser = getattr(playwright, _browser_name).launch(headless=HEADLESS, slow_mo=SLOWMO, args=_args)
    match _browser_name:
        case "chromium":
            _context = _browser.new_context(no_viewport=True, locale="en-US")
        case "firefox" | "webkit":
            _context = _browser.new_context(viewport={"width": 1280, "height": 720}, locale="en-US")
    _context.on("page", attach_page_listeners)
    yield _context
    _context.close()
    _browser.close()


@pytest.fixture
def init_page(init_context):
    """
    Give each test the shared context, and reset it after the test so the next test starts clean:
    extra tabs closed, localStorage/sessionStorage and cookies cleared, page back to blank.

    Args:
        init_context: Browser context shared by every test in the file.

    Returns:
        Browser: page of the browser with 'about:blank' url
    """
    _page = init_context.pages[0] if init_context.pages else init_context.new_page()
    yield _page
    _reset_page(init_context, _page)


def _reset_page(context: BrowserContext, page: Page):
    """
    Reset the shared tab so the next test starts clean.

    Args:
        context (BrowserContext): Browser context coming from init_page.
        page (Page): Page coming from init_page.
    """
    for _extra in [_other for _other in context.pages if _other is not page]:
        _extra.close()
    try:
        page.evaluate("() => { localStorage.clear(); sessionStorage.clear(); }")
    except Exception:
        pass  # e.g. the page is on about:blank, where there is no storage to clear
    context.clear_cookies()
    page.goto("about:blank")

import base64
import os, re, pytest, logging
from datetime import datetime
from config.config import BASEURL, PRACTICEURL

# Single logger for the whole framework. Import it everywhere with: from fixtures.logging_fixture import logger
# Output format and levels are configured in pytest.ini.
logger = logging.getLogger("automation")
_REPORT_DIR = "reports"
_DATE_TIME = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
_RUN_DIR = f"reports/{_DATE_TIME}"
_SCREENSHOT_DIR = f"{_RUN_DIR}/screenshots"


# -------------------------
# Log file
# -------------------------

def pytest_configure(config):
    """
    Give each run its own folder, reports/<timestamp>/, holding that run's HTML report
    (html/report<timestamp>.html) and log file (log/test_run<timestamp>.log).
    Overrides the --html and log_file values set in pytest.ini.

    Args:
        config: pytest config object.
    """
    config.option.htmlpath = f"{_RUN_DIR}/html/report{_DATE_TIME}.html"
    config.option.log_file = f"{_RUN_DIR}/log/test_run{_DATE_TIME}.log"


# -------------------------
# Test results
# -------------------------

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Log each test's result, duration and failure reason, and store the report on the test
    so fixtures can check whether it failed (used for screenshots on failure).

    Args:
        item: The test item being reported.
        call: Information about the test phase (setup, call or teardown).
    """
    _outcome = yield
    _report = _outcome.get_result()
    setattr(item, f"rep_{_report.when}", _report)
    _marker = item.get_closest_marker("description")
    _report.description = _marker.args[0] if _marker else ""
    if item.get_closest_marker("api"):
        _report.test_type = "API"
    elif item.get_closest_marker("ui"):
        _report.test_type = "UI"
    else:
        _report.test_type = "API" if "tests/api" in item.nodeid else "UI"

    if _report.when == "setup" and _report.failed:
        logger.error(f"SETUP FAILED | {item.name} | {call.excinfo.value}")

    if _report.when == "call":
        logger.info(f"RESULT: {_report.outcome.upper()} | {item.name} | {_report.duration:.2f}s")
        if _report.failed:
            logger.error(f"Failure reason: {call.excinfo.value}")
            _page = item.funcargs.get("init_page")
            if _page is None:
                logger.warning(f"No browser page found for {item.name}; screenshot skipped")
            else:
                _screenshots = save_failure_screenshots(_page.context, item.name)
                _attach_screenshots_to_report(item, _report, _screenshots)


def _attach_screenshots_to_report(item, report, screenshots: list[bytes]):
    """
    Embed screenshots in the HTML report for this test.

    Args:
        item: The test item.
        report: The test report to attach to.
        screenshots: PNG images as bytes.
    """
    _html = item.config.pluginmanager.getplugin("html")
    if not _html:
        return
    _extras = getattr(report, "extras", [])
    for _png in screenshots:
        _extras.append(_html.extras.png(base64.b64encode(_png).decode()))
    report.extras = _extras


# -------------------------
# Run and test boundaries
# -------------------------

@pytest.fixture(scope="session", autouse=True)
def log_run_info(request):
    """
    Log the browser and environment once at the start of the run.

    Args:
        request: pytest request object for the session.
    """
    logger.info("=" * 60)
    logger.info(f"Browser: {request.config.getoption('--web-browser')}")
    logger.info(f"Base URL: {BASEURL}")
    logger.info(f"Practice URL: {PRACTICEURL}")
    logger.info("=" * 60)


@pytest.fixture(autouse=True)
def log_test_boundaries(request):
    """
    Log the start, description and end of every test.

    Args:
        request: pytest request object for the current test.
    """
    logger.info(f"========== START: {request.node.name} ==========")
    _marker = request.node.get_closest_marker("description")
    if _marker:
        logger.info(f"Description: {_marker.args[0]}")
    yield
    logger.info(f"========== END: {request.node.name} ==========")


# -------------------------
# Browser helpers (called from browser_fixture.py)
# -------------------------

def attach_page_listeners(page):
    """
    Log browser console errors and uncaught JavaScript errors for a page.

    Args:
       page: Playwright page to listen on.
    """

    def _log_console_error(message):
        if message.type == "error":
            logger.warning(f"Browser console error: {message.text}")

    page.on("console", _log_console_error)
    page.on("pageerror", lambda error: logger.warning(f"Page JavaScript error: {error}"))


def save_failure_screenshots(context, test_name: str):
    """
    Save a full-page screenshot of every open tab and log each path.

    Args:
        context: Browser context whose tabs are captured.
        test_name: Name of the failed test, used in the file names.
    """
    os.makedirs(_SCREENSHOT_DIR, exist_ok=True)
    _safe_name = re.sub(r"[^\w\-\[\]]", "_", test_name)
    _images = []
    for _index, _page in enumerate(context.pages):
        _path = f"{_SCREENSHOT_DIR}/{_safe_name}_{_index}.png"
        try:
            _images.append(_page.screenshot(path=_path, full_page=True))
            logger.error(f"Screenshot saved: {_path}")
        except Exception as error:
            logger.warning(f"Could not save screenshot for tab {_index}: {error}")
    return _images

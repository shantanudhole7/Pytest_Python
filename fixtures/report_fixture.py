import base64
import html
import re
from pathlib import Path
import pytest
from pytest_metadata.plugin import metadata_key
from config.config import BASEURL, PRACTICEURL, APIBASEURL, REPORTLOGO, REPORTTABTITLE

# Environment entries added by pytest-metadata that should not appear in the report.
_HIDDEN_METADATA = ["Platform", "JAVA_HOME", "Plugins", "Python", "Packages", "Base URL"]
_LOGO_TYPES = {".svg": "image/svg+xml", ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg"}


def pytest_collection_finish(session):
    """
    Fill the Environment section of the HTML report from the tests that will actually run,
    so a run of one file, a -k filter or a -m marker all show the right test type, URLs and browser.

    Runs after collection, which is also after pytest-base-url has written its empty "Base URL" entry,
    so the hidden entries are removed here too.

    Args:
        session: pytest session object, with the selected tests in session.items.
    """
    _metadata = session.config.stash[metadata_key]
    for _key in _HIDDEN_METADATA:
        _metadata.pop(_key, None)
    if not session.items:
        return

    _types = {test_type(_item) for _item in session.items}
    _fixtures = {_name for _item in session.items for _name in _item.fixturenames}

    if "API" in _types:
        _metadata["API BASE URL"] = APIBASEURL
    if "login_page" in _fixtures:
        _metadata["UI BASE URL"] = BASEURL
    if "navigate_url" in _fixtures:
        _metadata["PRACTICE URL"] = PRACTICEURL
    _metadata["Test Type"] = "All Tests (API + UI)" if _types == {"API", "UI"} else f"{_types.pop()} Tests"
    if "UI" in _types or "login_page" in _fixtures or "navigate_url" in _fixtures:
        _metadata["Browser"] = session.config.getoption("--web-browser")


def test_type(item) -> str:
    """
    Return "API" or "UI" for a test: from its ui/api marker, or from its folder when it has neither.

    Args:
        item: pytest test item.

    Returns:
        str: "API" or "UI".
    """
    if item.get_closest_marker("api"):
        return "API"
    if item.get_closest_marker("ui"):
        return "UI"
    return "API" if "tests/api" in item.nodeid.replace("\\", "/") else "UI"

def pytest_html_report_title(report):
    """
    Set the HTML report title.
    """
    report.title = "PytestPython – UI and API Tests Report"


def pytest_html_results_table_header(cells):
    """
    Add a Description column to the results table.
    """
    cells.insert(2, "<th>Description</th>")
    for i, cell in enumerate(cells):
        if "Links" in cell:
            cells[i] = "<th>Test Type</th>"


def pytest_html_results_table_row(report, cells):
    """
    Shorten the Test column to Class::test (without the file path) and fill the Description column.

    Example: tests/ui/test_login_page.py::TestLoginPage::test_login_shows_error[locked_user]
             becomes TestLoginPage::test_login_shows_error[locked_user]
    """
    for i, cell in enumerate(cells):
        if "col-links" in cell:
            cells[i] = f'<td class="col-test-type">{getattr(report, "test_type", "")}</td>'
    _short_name = report.nodeid.split("::", 1)[-1]
    for _index, _cell in enumerate(cells):
        if 'class="col-testId"' in _cell:
            cells[_index] = f'<td class="col-testId">{html.escape(_short_name)}</td>'
            break
    cells.insert(2, f"<td>{html.escape(getattr(report, 'description', ''))}</td>")


@pytest.hookimpl(tryfirst=True)
def pytest_unconfigure(config):
    """
    Brand the HTML report after pytest-html has written it, using the [report] settings in config.ini:
    the browser tab shows tab_title and the logo as its icon, and the logo appears next to the report title.
    The logo is embedded, so the report stays self-contained. A missing or unsupported logo is logged
    and the rest of the report is left unchanged.

    Args:
        config: pytest config object.
    """
    if hasattr(config, "workerinput"):
        return
    _report = Path(config.option.htmlpath or "")
    if not _report.is_file():
        return
    _html = _report.read_text(encoding="utf-8")

    if REPORTTABTITLE:
        _html = re.sub(r'(<title id="head-title">).*?(</title>)',
                       lambda _match: f"{_match.group(1)}{html.escape(REPORTTABTITLE)}{_match.group(2)}",
                       _html, count=1, flags=re.S)

    _logo = Path(config.rootpath) / REPORTLOGO if REPORTLOGO else None
    _mime = _LOGO_TYPES.get(_logo.suffix.lower()) if _logo else None
    if _logo and _logo.is_file() and _mime:
        _src = f"data:{_mime};base64,{base64.b64encode(_logo.read_bytes()).decode()}"
        _html = _html.replace("<head>", f'<head>\n    <link rel="icon" type="{_mime}" href="{_src}">', 1)
        _html = re.sub(r'(<h1 id="title">.*?</h1>)',
                       lambda _match: f'<div class="pp-brand"><img class="pp-logo" src="{_src}" alt="">'
                                      f'{_match.group(1)}</div>',
                       _html, count=1, flags=re.S)
    _report.write_text(_html, encoding="utf-8")
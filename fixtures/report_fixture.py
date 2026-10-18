import html
from pytest_metadata.plugin import metadata_key
from config.config import BASEURL, PRACTICEURL, APIBASEURL

# Environment entries added by pytest-metadata that should not appear in the report.
_HIDDEN_METADATA = ["Platform", "JAVA_HOME", "Plugins", "Python", "Packages", "Base URL"]


def pytest_sessionstart(session):
    """
    Add run details to the Environment section of the HTML report.

    Runs at session start, after every plugin's pytest_configure. pytest-base-url
    (installed with pytest-playwright) writes its own empty "Base URL" entry during
    configure, so setting ours here makes sure our value is the one shown.

    Args:
        session: pytest session object.
    """
    _metadata = session.config.stash[metadata_key]
    for _key in _HIDDEN_METADATA:
        _metadata.pop(_key, None)
    _marker = session.config.getoption("-m")
    if not _marker:
        _metadata["API BASE URL"] = APIBASEURL
        _metadata["UI BASE URL"] = BASEURL
        _metadata["PRACTICE URL"] = PRACTICEURL
        _metadata["Test Type"] = "All Tests (API + UI)"
        _metadata["Browser"] = session.config.getoption("--web-browser")
    elif _marker == "api":
        _metadata["BASE URL"] = APIBASEURL
        _metadata["Test Type"] = "API Tests"
    else:
        _metadata["BASE URL"] = PRACTICEURL if _marker == "dialog" else BASEURL
        _metadata["Test Type"] = "UI Tests"
        _metadata["UI Tests Browser"] = session.config.getoption("--web-browser")


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

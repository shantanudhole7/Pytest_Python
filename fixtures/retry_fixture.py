"""
Retry failed tests at the end of the run, in their original order.

Every test runs once first. A test that fails (in setup or in the test itself) is reported as RERUN
and queued; once all tests have run, the queued tests run again in collection order. A test that
passes on retry counts as passed; one that fails its last retry counts as failed.

Number of retries: [execution] retries in config.ini, or --retries N for one run (0 turns it off).
"""
import pytest
from config.config import RETRIES
from fixtures.logging_fixture import logger

_ATTEMPT = pytest.StashKey[int]()
_QUEUED = pytest.StashKey[bool]()


def pytest_addoption(parser):
    """
    Add the --retries option.

    Args:
        parser: pytest command-line parser.
    """
    parser.addoption("--retries", action="store", type=int, default=None,
                     help="Retry failed tests this many times after the whole run "
                          "(default: [execution] retries in config.ini; 0 turns it off).")


def _max_retries(config) -> int:
    """
    Return the number of retries: --retries if given, otherwise RETRIES from config.ini.

    Args:
        config: pytest config object.

    Returns:
        int: Number of retry rounds, 0 or more.
    """
    _option = config.getoption("--retries")
    return RETRIES if _option is None else max(_option, 0)


@pytest.hookimpl(tryfirst=True)
def pytest_runtestloop(session):
    """
    Replace pytest's run loop: run every test once, then retry the failed ones after the whole run,
    in collection order, for up to the configured number of rounds.

    Args:
        session: pytest session object.

    Returns:
        bool: True, so pytest's default run loop does not run as well.
    """
    if session.testsfailed and not session.config.option.continue_on_collection_errors:
        raise session.Interrupted(f"{session.testsfailed} error(s) during collection")
    if session.config.option.collectonly:
        return True

    _run_items(session, session.items)

    for _round in range(1, _max_retries(session.config) + 1):
        _queued = [_item for _item in session.items if _item.stash.get(_QUEUED, False)]
        if not _queued:
            break
        logger.info("=" * 60)
        logger.info(f"RETRY ROUND {_round} | {len(_queued)} test(s): {', '.join(_item.name for _item in _queued)}")
        logger.info("=" * 60)
        for _item in _queued:
            _item.stash[_QUEUED] = False
            _item.stash[_ATTEMPT] = _item.stash.get(_ATTEMPT, 0) + 1
            _item._initrequest()  # fresh fixture request, as pytest-rerunfailures does
        _run_items(session, _queued)
    return True


def _run_items(session, items: list):
    """
    Run the given tests in order, the same way pytest's default loop does.
    The last test tears down every fixture, so a retry round starts with fresh fixtures.

    Args:
        session: pytest session object.
        items: Tests to run, in order.
    """
    for _index, _item in enumerate(items):
        _next_item = items[_index + 1] if _index + 1 < len(items) else None
        _item.config.hook.pytest_runtest_protocol(item=_item, nextitem=_next_item)
        if session.shouldfail:
            raise session.Failed(session.shouldfail)
        if session.shouldstop:
            raise session.Interrupted(session.shouldstop)


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """
    Turn a failure into RERUN and queue the test while it has retries left.
    Runs after logging_fixture's hook, so the failure is still logged and screenshotted.

    Args:
        item: The test item being reported.
        call: Information about the test phase (setup, call or teardown).
    """
    _outcome = yield
    _report = _outcome.get_result()
    if _report.when in ("setup", "call") and _report.failed and not hasattr(_report, "wasxfail"):
        _attempt = item.stash.get(_ATTEMPT, 0)
        _max = _max_retries(item.config)
        if _attempt < _max:
            _report.outcome = "rerun"
            item.stash[_QUEUED] = True
            logger.warning(f"RETRY QUEUED | {item.name} | retry {_attempt + 1} of {_max} after all tests finish")


def pytest_report_teststatus(report):
    """
    Show queued failures as R / RERUN in the console instead of F / FAILED.

    Args:
        report: The test report.
    """
    if report.outcome == "rerun":
        return "rerun", "R", ("RERUN", {"yellow": True})
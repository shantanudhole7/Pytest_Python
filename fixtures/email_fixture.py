"""
Email the reporting-labs report (PDF and HTML) once a run has finished and the report has been written.

Switched on per run with --send-email, or for every run with EMAILENABLED=true in .env.
SMTP settings and recipients come from .env through config/config.py.
"""
import html
import smtplib
import ssl
import time
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path
import pytest
from config.config import EMAILENABLED, SMTPHOST, SMTPPORT, SMTPUSER, SMTPPASSWORD, EMAILFROM, EMAILTO
from fixtures.logging_fixture import logger

_MAX_ATTACHMENT_MB = 20
_REPORT_DIR = "reporting-labs"
_RUN = {"start": time.time(), "exit_status": None}


def pytest_addoption(parser):
    """
    Add the --send-email option.

    Args:
        parser: pytest command-line parser.
    """
    parser.addoption("--send-email", action="store_true", default=False,
                     help="Email the reporting-labs report to EMAILTO when the run finishes.")


def pytest_sessionfinish(exitstatus):
    """
    Remember the run's exit status for the email subject.

    Args:
        exitstatus: Exit code of the run.
    """
    _RUN["exit_status"] = int(exitstatus)


@pytest.hookimpl(trylast=True)
def pytest_unconfigure(config):
    """
    Send the report email. Runs after pytest_sessionfinish, so pytest-html has already written the report.
    A failure to send is logged and never changes the run's result.

    Args:
        config: pytest config object.
    """
    if hasattr(config, "workerinput"):
        return
    if not (config.getoption("--send-email", default=False) or EMAILENABLED):
        return

    _recipients = [_address.strip() for _address in (EMAILTO or "").split(",") if _address.strip()]
    _missing = [_name for _name, _value in [("SMTPHOST", SMTPHOST), ("SMTPUSER", SMTPUSER),
                                            ("SMTPPASSWORD", SMTPPASSWORD), ("EMAILTO", _recipients)]
                if not _value]
    if _missing:
        logger.warning(f"Report email not sent | Missing in .env: {', '.join(_missing)}")
        return

    try:
        _message = build_report_email(config, _recipients)
        _send(_message)
        logger.info(f"Report email sent to {', '.join(_recipients)}")
    except Exception as error:
        logger.warning(f"Report email not sent | {type(error).__name__}: {error}")


def _run_counts(config) -> dict:
    """
    Count test results from pytest's terminal reporter.

    Args:
        config: pytest config object.

    Returns:
        dict: Number of tests per outcome.
    """
    _reporter = config.pluginmanager.get_plugin("terminalreporter")
    _stats = getattr(_reporter, "stats", {}) or {}
    _counts = {_key: len(_stats.get(_key, [])) for _key in ("passed", "failed", "error", "skipped", "rerun")}
    _counts["total"] = _counts["passed"] + _counts["failed"] + _counts["error"] + _counts["skipped"]
    return _counts


def _reporting_labs_files(config) -> list[Path]:
    """
    Return the reporting-labs report files written by this run: the PDF and the HTML page.
    Files older than the run start are left out, so a failed run never sends an old report.

    Args:
        config: pytest config object.

    Returns:
        list[Path]: Report files to attach, PDF first.
    """
    _folder = Path(config.rootpath) / _REPORT_DIR
    _files = [_folder / "report.pdf", _folder / "index.html"]
    return [_file for _file in _files if _file.is_file() and _file.stat().st_mtime >= _RUN["start"]]

def _summary_table(rows: list[tuple]) -> str:
    """
    Build the run summary as a bordered HTML table for the email body.
    Inline styles only, because most email clients ignore <style> blocks.

    Args:
        rows: (label, value) pairs to show.

    Returns:
        str: The HTML table.
    """
    _border = "border:1px solid #d0d7de"
    _cell = f"{_border};padding:8px 14px;text-align:left"
    _header = (f"<tr style='background:#24292f;color:#ffffff'>"
               f"<th style='{_cell};font-weight:600'>Metric</th>"
               f"<th style='{_cell};font-weight:600'>Value</th></tr>")

    _body = "".join(
        f"<tr style='background:{'#f6f8fa' if _index % 2 else '#ffffff'}'>"
        f"<td style='{_cell};color:#57606a'>{html.escape(str(_label))}</td>"
        f"<td style='{_cell};font-weight:600;color:#57606a'>{html.escape(str(_value))}</td>"
        f"</tr>"
        for _index, (_label, _value) in enumerate(rows)
    )
    return (f"<table style='border-collapse:collapse;{_border};min-width:320px'>"
            f"{_header}{_body}</table>")


def build_report_email(config, recipients: list[str]) -> EmailMessage:
    """
    Build the email: a result summary in the body and the reporting-labs report (PDF and HTML) attached.

    Args:
        config: pytest config object.
        recipients: Email addresses to send to.

    Returns:
        EmailMessage: The message, ready to send.
    """
    _counts = _run_counts(config)
    _status = "FAILED" if (_counts["failed"] or _counts["error"] or _RUN["exit_status"] not in (0, None)) \
        else "PASSED"
    _duration = time.time() - _RUN["start"]
    _finished = datetime.now().strftime("%Y-%m-%d %H:%M")
    _marker = config.getoption("-m", default="") or "all tests"

    _rows = [
        ("Finished", _finished),
        ("Duration", f"{_duration / 60:.1f} min"),
        ("Tests run", f"{_counts['total']} ({_marker})"),
        ("Passed", _counts["passed"]),
        ("Failed", _counts["failed"]),
        ("Errors", _counts["error"]),
        ("Skipped", _counts["skipped"]),
    ]
    if _counts["rerun"]:
        _rows.append(("Reruns", _counts["rerun"]))

    _message = EmailMessage()
    _message["Subject"] = f"Framework - Pytest_Product : Execution Report – {_finished}"

    _message["From"] = EMAILFROM or SMTPUSER
    _message["To"] = ", ".join(recipients)

    _attachments, _too_large = [], []
    _total_mb = 0.0
    for _file in _reporting_labs_files(config):
        _size_mb = _file.stat().st_size / (1024 * 1024)
        if _total_mb + _size_mb <= _MAX_ATTACHMENT_MB:
            _attachments.append(_file)
            _total_mb += _size_mb
        else:
            _too_large.append(_file)

    if _attachments:
        _note = ("Attached: the execution report as PDF (quick view) and HTML (full interactive report, "
                 "open it in a browser).") if len(_attachments) == 2 else f"Attached: {_attachments[0].name}."
    else:
        _note = "No execution report report was written by this run."
    if _too_large:
        _note += " Too large to attach, saved at: " + ", ".join(str(_file.resolve()) for _file in _too_large)

    _text = "\n".join(f"{_label}: {_value}" for _label, _value in _rows)
    _table = _summary_table(_rows)

    # Order matters: plain text, then the HTML alternative, then the attachments.
    _message.set_content(f"Framework - Pytest_Product test run\n\n{_text}\n\n{_note}\n")
    _message.add_alternative(
        f"<div style='font-family:Calibri (Body),Arial,sans-serif;font-size:14px'>"
        f"<h2 style='margin:0 0 12px;color:#064273'>Framework - Pytest_Product : Detail Execution Report</h2>"
        f"{_table}"
        f"<p style='color:#555'>{html.escape(_note)}</p></div>",
        subtype="html",
    )
    for _file in _attachments:
        _maintype, _subtype = ("application", "pdf") if _file.suffix == ".pdf" else ("text", "html")
        _message.add_attachment(_file.read_bytes(), maintype=_maintype, subtype=_subtype,
                                filename=f"reporting-labs-{_file.name}")
    return _message


def _send(message: EmailMessage):
    """
    Send the message over SMTP: implicit TLS on port 465, STARTTLS otherwise.

    Args:
        message: The email to send.
    """
    _context = ssl.create_default_context()
    if SMTPPORT == 465:
        with smtplib.SMTP_SSL(SMTPHOST, SMTPPORT, context=_context, timeout=30) as _server:
            _server.login(SMTPUSER, SMTPPASSWORD)
            _server.send_message(message)
    else:
        with smtplib.SMTP(SMTPHOST, SMTPPORT, timeout=30) as _server:
            _server.starttls(context=_context)
            _server.login(SMTPUSER, SMTPPASSWORD)
            _server.send_message(message)

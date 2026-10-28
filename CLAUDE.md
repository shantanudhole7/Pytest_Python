# CLAUDE.md — PytestPython

Playwright + pytest framework that tests UI (Sauce Demo, practice-automation.com) and API (Rahul Shetty Academy
e-commerce).
Study project; the long-term goal is a reusable framework, including a report setup others can adopt without writing
report code.

- Full architecture, fixtures and examples: `README.md`. Read it before large changes.
- Coding standards: the `best-practices` skill (`.claude/skills/best-practice/SKILL.md`). Follow it for every test, page
  object, API class, POJO, fixture or locator.
- Reviews: `/test-review` (all tests) or `/test-review <file>`.

## Rules for Claude (most important)

- **Never change code or files without my consent.** Show the proposed change (diff or full snippet) and explain why;
  edit only after I explicitly say yes.
- **Ask before running tests.** `[email] enabled = true` in `config/config.ini`, so every pytest run emails the report
  to the addresses in `EMAILTO`.
- Never read, print, log or commit `.env` values. Never move secrets into `config.ini` or code.
- Don't add or upgrade dependencies without asking.
- After a change, tell me the exact command to verify it (one file or one test, not the whole suite).
- When we make a decision, propose a line for the Decisions log below.

## Environment

- Python 3.10+ (code uses `match` and `str | None`), PyCharm project, `.venv` in the project root.
- No `requirements.txt` yet. Install:
  `python -m pip install pytest pytest-playwright python-dotenv pytest-html pytest-metadata reporting-labs` then
  `python -m playwright install`.
- Run every command from the `PytestPython` folder so `pytest.ini` and `conftest.py` are picked up.
- Retries: failed tests are retried after the whole run (`[execution] retries` in `config.ini`); `--retries N` for one
  run, `--retries 0` to turn off

## Commands

- All tests: `python -m pytest`
- By layer: `python -m pytest -m ui` / `-m api`
- One file: `python -m pytest tests/ui/test_login_page.py`
- One test: `python -m pytest tests/ui/test_login_page.py::TestLoginPage::test_valid_user_login`
- Other browser: `--web-browser firefox` (`chromium` default, `firefox`, `webkit`)
- Email the report for one run: `--send-email`

## Layout

- `pages/` page objects (inherit `BasePage`); `pages/core/` element wrappers `BaseElement`, `Input`, `Button`, `Label`,
  `Dialog`
- `api/` API classes (inherit `ApiBase`); `pojo/` dataclasses for request bodies; `data/` JSON payloads and shared test
  data
- `fixtures/` pytest plugins registered in `conftest.py` via `pytest_plugins` (tests never import fixture modules)
- `config/config.ini` non-secret settings; `config/config.py` exposes UPPERCASE constants; `.env` secrets only
- `tests/ui/`, `tests/api/`, `tests/base_test.py` (`BaseTest` + `log_information` and `assert_*` helpers)
- `utils/Assertions/assertion.py` PASS/FAIL logging
- Generated, never edit: `reports/<timestamp>/`, `reporting-labs/`, `reporting-labs.history.json`

## Conventions (summary; the skill has the full detail)

- Files `test_<page_name>.py`, classes `Test<PageName>(BaseTest)`, methods `test_<behaviour>`, local variables prefixed
  `_`.
- Locators only in page-object constructors, wrapped in a core element, named with a type prefix: `input_`, `btn_`,
  `lbl_`, `lnk_`, `alert_`.
- Navigation methods return the next page object (e.g. `LoginPage.login()` returns `ProductPage`).
- No locators or hard-coded values in tests. Per-file values are UPPERCASE class constants; shared settings in
  `config.ini`; structured data in `data/`.
- Assert only through `tests/base_test.py` helpers (`assert_equal`, `assert_text`, `assert_displayed`, `assert_count`,
  `assert_url`, `assert_http_ok`), never bare `assert` in tests.
- No `time.sleep()` or `wait_for_timeout()`; rely on auto-waiting and `expect`.
- Every test has: `@pytest.mark.description("Verify ...")`, `ui` or `api`, one severity marker (`blocker`/`critical`/
  `major`/`minor`/`trivial`), and the reporting-labs docstring `"""@priority P1 @owner Shantanu @feature <area>"""`.
- New markers must be registered in `pytest.ini` (`--strict-markers` is on).
- `config.ini` values are written without quotes.

## Gotchas

- One browser per test file (`init_context`, module scope); all tests in the file share one tab, reset after each test
  by `init_page`. A test that passes alone but fails in the file run usually leaks state the reset doesn't cover.
- Because the tab is shared, dialog handlers must be one-time: `Dialog.accept_next()` / `dismiss_next()` use
  `page.once`, never `page.on`.
- Test-id attribute is `data-test` (set in `browser_fixture.py`), so use `get_by_test_id(...)` for Sauce Demo.
- Browsers run headed with `slow_mo=300` (`[browser]` in `config.ini`).
- API: `auth` is session-scoped (one login per run). Products from `create_product` are deleted after the test; mark
  `skip_teardown` when the test deletes them itself.
- A failed report email is only logged as a warning and never fails the run.
- A failed test is reported as RERUN and retried only after all tests have run, with fresh fixtures (new browser, new
  API login). Code that depends on test order or shared state must survive a test running again at the end.

## Decisions log

Add one line per decision so future sessions keep it.

- 2026-10-24: Created this CLAUDE.md.
- 2026-10-27: PracticePage (WEBFORMURL) tests are split per widget (test_radio_page.py / TestRadioPage,
  test_checkbox_page.py / TestCheckboxPage, ...), an agreed exception to test_<page_name>.py.
- 2026-10-28: Failed tests are retried after the whole run, in original order (`fixtures/retry_fixture.py`), not
  immediately as pytest-rerunfailures does.
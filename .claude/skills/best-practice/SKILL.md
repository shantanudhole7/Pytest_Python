---
name: best-practices
description: Playwright + pytest UI and API test automation standards for this project — project layout, naming,
  configuration and test data, locator strategy, Page Object Model with core element wrappers, API layer,
  fixtures and the shared browser, test structure, assertions, and waits. Use this skill whenever writing,
  generating, reviewing, refactoring, or debugging any test, page object, core element, API class, POJO,
  fixture, or locator in this project, even if the request doesn't mention "best practices".
user-invocable: false
---

# Playwright Test Automation Best Practices

These are the standards for all UI and API tests in this project. Follow them when writing new code and flag
deviations when reviewing existing code. Where a rule's reason isn't obvious, it's given so you can apply it
sensibly to cases not covered here.

---

## 1. Project Layout

All paths are relative to the project root (`PytestPython/`), which is the sources root and the directory
pytest is run from.

```
PytestPython/
├── api/                          # API request classes (non-test code)
│   ├── api_base.py               # ApiBase: send + log requests, load JSON payloads
│   └── <name>_api.py             # One class per endpoint group, e.g. create_order_api.py
├── assets/
│   └── report.css                # Theme for the pytest-html report
├── config/
│   ├── config.ini                # Settings safe to commit: URLs, demo users, messages, SMTP host/port
│   └── config.py                 # Reads config.ini + .env, exposes UPPERCASE constants
├── data/                         # Structured test data (see §3)
│   ├── <name>.py                 # Python data modules, e.g. product.py
│   ├── <name>_api.json           # API request payloads, e.g. create_order_api.json
│   └── files/                    # Files used by tests, e.g. upload images
├── fixtures/                     # pytest plugins, registered in conftest.py
│   ├── logging_fixture.py        # Logger, per-run report/log paths, results, failure screenshots
│   ├── browser_fixture.py        # --web-browser, init_context, init_page
│   ├── page_fixture.py           # login_page, navigate_url, url
│   ├── api_fixture.py            # api_context, auth, create_product, delete_product
│   ├── report_fixture.py         # pytest-html title, Environment table, extra columns
│   └── email_fixture.py          # --send-email, emails the report after the run
├── pages/
│   ├── core/                     # Element wrappers: BaseElement, Input, Button, Label, Dialog
│   ├── base_page.py              # BasePage: common actions for all page objects
│   └── <page_name>_page.py       # One page object per screen, e.g. login_page.py
├── pojo/
│   └── <name>.py                 # Dataclasses that build API request bodies, e.g. create_order.py
├── tests/
│   ├── base_test.py              # BaseTest + log_information and assert_* functions (not a test file)
│   ├── api/
│   │   └── test_<name>_api.py    # API test files
│   └── ui/
│       └── test_<page_name>.py   # UI test files, e.g. test_login_page.py
├── utils/
│   └── Assertions/               # Assertion: logger_info / logger_error (PASS/FAIL lines)
├── .env                          # Secrets only: API login, email account (never commit)
├── conftest.py                   # Root conftest: registers fixtures from fixtures/
└── pytest.ini                    # Markers, report options, logging
```

### Where new files go
| New item             | Location                                 | Class                              |
|----------------------|------------------------------------------|------------------------------------|
| Page object          | `pages/<page_name>_page.py`              | `<PageName>Page(BasePage)`         |
| Element wrapper      | `pages/core/<element>.py`                | `<Element>(BaseElement)`           |
| API class            | `api/<name>_api.py`                      | `<Name>Api(ApiBase)`               |
| Request body (POJO)  | `pojo/<name>.py`                         | `@dataclass <Name>`                |
| UI test              | `tests/ui/test_<page_name>.py`           | `Test<PageName>(BaseTest)`         |
| API test             | `tests/api/test_<name>_api.py`           | `Test<Name>Api(BaseTest)`          |
| Fixture module       | `fixtures/<type>_fixture.py`             | — (register in root `conftest.py`) |
| Assertion helper     | `tests/base_test.py` (see §7)            | method on `BaseTest` + function    |
| Setting              | `config/config.ini` + `config/config.py` | —                                  |
| Secret               | `.env` + `config/config.py`              | —                                  |
| Structured test data | `data/<name>.py` or `data/<name>.json`   | —                                  |
| Test file / upload   | `data/files/`                            | —                                  |

### Rules
- Fixtures in `fixtures/` are not auto-discovered by pytest. Register each module in the root `conftest.py`:
```python
pytest_plugins = ["fixtures.logging_fixture", "fixtures.browser_fixture", ...]
```
- Never import fixtures into test files (`from fixtures.browser_fixture import init_page`). Pytest injects them
  by parameter name; importing them duplicates the fixture and can cause confusing errors.
- `tests/base_test.py` is the shared base class and assertion module for UI and API tests, not a test file.
  Do not rename it, add tests to it, or create a `test_base.py`.
- Do not create additional `conftest.py` files unless a fixture is genuinely specific to one test folder.
- Do not modify `pytest.ini` or `base_test.py` unless the task explicitly asks for it.

---

## 2. Naming Conventions

| Item                          | Convention                                       | Example                                          |
|-------------------------------|--------------------------------------------------|--------------------------------------------------|
| Test file                     | `test_<page_name>.py`, snake_case                | `test_login_page.py`, `test_create_order_api.py` |
| Page file                     | `<page_name>_page.py`                            | `login_page.py`                                  |
| API file                      | `<name>_api.py`                                  | `create_order_api.py`                            |
| Fixture file                  | `<type>_fixture.py`                              | `browser_fixture.py`                             |
| Test class                    | `Test` + PascalCase name, matching the file      | `TestLoginPage`, `TestCreateOrderApi`            |
| Base test class               | `BaseTest` (never `TestBase`)                    | `BaseTest`                                       |
| Test method                   | `test_<behaviour>`, snake_case                   | `test_valid_user_login`, `test_invalid_password` |
| Page / helper method          | verb first, snake_case                           | `login`, `get_error_message`                     |
| Local variable                | `_` prefix, snake_case                           | `_page`, `_login_page`, `_error_message`         |
| Page-object element attribute | element-type prefix, snake_case                  | `input_username`, `btn_login`                    |
| Config constant               | UPPERCASE, defined in `config/config.py`         | `BASEURL`, `APPUSERNAME`                         |
| Test-class constant           | UPPERCASE, defined at the top of the test class  | `FIRST_NAME_ERROR_MESSAGE`                       |

Element-type prefixes: `input_`, `btn_`, `alert_`, `lnk_`, `chk_`, `lbl_`, `drp_`, `lst_` (a list of items).

Avoid generic names like `test1`, `data`, or `btn`.

### Test class rules
- One test class per test file, inheriting from `BaseTest`.
- Base classes must not start with `Test`, or pytest will try to collect them.
- Test classes must not define `__init__` — pytest silently skips such classes. Use fixtures for setup.

---

## 3. Configuration and Test Data

Choose by who uses the value and whether it may be published: the narrowest place that covers every user
wins, and anything tied to a real account goes in `.env`.

| Kind of value                           | Examples                                                         | Lives in                               |
|-----------------------------------------|------------------------------------------------------------------|----------------------------------------|
| Secrets                                 | Your API login, Gmail address and app password, email recipients | `.env`                                 |
| Settings safe to commit                 | URLs and paths, public demo users, shared messages, SMTP host    | `config/config.ini`                    |
| Structured data shared by several files | Parametrize datasets, API payload templates, upload files        | `data/`                                |
| Values used by one test file only       | Expected messages, form input, product picks for that page       | UPPERCASE constants on that test class |

`config/config.py` is the only code that reads `config.ini` and `.env`; everything else imports its
UPPERCASE constants, so a setting changes in one file and secrets never appear in code. `data/` keeps
multi-field datasets out of `config.ini`, so it stays a flat list of settings. Test-class constants keep
values next to the only tests that use them, so `config.ini` doesn't fill up with one-off strings.

```python
# tests/ui/test_e2e_scenario_page.py — DO: values only this file uses
class TestE2EScenarioPage(BaseTest):
    FIRST_NAME_ERROR_MESSAGE = "Error: First Name is required"
    LAST_NAME_ERROR_MESSAGE = "Error: Last Name is required"
```

```ini
; config/config.ini — sections in lowercase snake_case, values without quotes
[url]
base_url = https://www.saucedemo.com

[credentials]
app_username = standard_user
```

```python
# config/config.py — one UPPERCASE constant per key
BASEURL = _ini.get("url", "base_url")
APPUSERNAME = _ini.get("credentials", "app_username")
APIUSERPASSWORD = os.getenv("APIUSERPASSWORD")   # secret, from .env
```

```python
# tests/ui/test_login_page.py — DO
from config.config import BASEURL, APPUSERNAME, PASSWORD
```

```python
# DON'T — hardcoded URL and credentials
_login_page.navigate("https://www.saucedemo.com")
_login_page.login("standard_user", "secret_sauce")
```

- Add a new setting to `config.ini` under the matching section and expose it in `config.py` with `_ini.get`
  (`getint` / `getboolean` for numbers and flags). Add a secret to `.env` and expose it with `os.getenv`.
- Write `config.ini` values without quotes; configparser keeps quotes as part of the value. Keys are
  case-insensitive, so use lowercase snake_case.
- Read `config.ini` without defaults: a missing key should stop the run at start-up (`NoOptionError`) rather
  than give `None` and fail later in a test.
- Never inline a value inside a test method. Name it, either as a test-class constant or in `config.ini` /
  `data/`, so the test reads as intent and the value changes in one place.
- Test-class constants are UPPERCASE, defined at the top of the class, and used only by that class. Once a
  second test file needs the value, move it to `config/config.ini` or `data/`.
- Inside a test method, read a class constant as `self.NAME`; in a decorator such as `parametrize` (which runs
  in the class body), use the bare `NAME`.
- Never put secrets or environment-specific values (URLs, credentials) in test-class constants.
- Import constants explicitly — no `from config.config import *`, which hides where names come from.
- Never put a secret in `config.ini` or give it a default value in `config.py`.
- `.env` is in `.gitignore`; commit a `.env.example` with the variable names and dummy values.
- Use `@pytest.mark.parametrize` for data-driven cases instead of duplicating tests. Use `pytest.param(...,
  id="...")` or `ids=[...]` so every case has a readable name in the report.

### Structured test data in `data/`
- Python data modules (`data/<name>.py`) hold datasets that tests parametrize over. Name the constant in
  UPPERCASE and import it explicitly: `from data.product import PRODUCTS`.
- JSON files (`data/<name>_api.json`) hold API request payloads, loaded through the API helper
  (`ApiBase.load_payload`), never with ad-hoc `open()` calls in tests. Values that change per run (ids,
  tokens) are set by the API class at runtime, not stored in the file.
- Files used by tests (images to upload, documents) go in `data/files/`.
- Never put secrets or settings (URLs, credentials) in `data/`; those belong in `.env` or `config.ini`.
- Define each dataset once and derive variants from it (e.g. names only, first two items) rather than
  repeating the same values in several tests.

---

## 4. Locator Strategy

Prefer locators based on what the user sees; they survive markup and styling changes far better than
structural selectors.

### Priority order
Use the first strategy that uniquely identifies the element.

| Priority | Strategy                           | Example                                    | Use for                                               |
|----------|------------------------------------|--------------------------------------------|-------------------------------------------------------|
| 1        | `get_by_role`                      | `page.get_by_role("button", name="Login")` | Buttons, links, checkboxes, headings, alerts, dialogs |
| 2        | `get_by_label`                     | `page.get_by_label("Email")`               | Form fields with a visible `<label>`                  |
| 3        | `get_by_placeholder`               | `page.get_by_placeholder("Username")`      | Inputs without a label                                |
| 4        | `get_by_text`                      | `page.get_by_text("Forgot password?")`     | Non-interactive text, messages                        |
| 5        | `get_by_alt_text` / `get_by_title` | `page.get_by_alt_text("Company logo")`     | Images, icons                                         |
| 6        | `get_by_test_id`                   | `page.get_by_test_id("add-to-cart")`       | When no user-facing attribute is stable or unique     |
| 7        | Stable ID or short attribute CSS   | `page.locator("input[name='otp']")`        | Last resort                                           |

The browser fixture already sets `data-test` as the test-id attribute
(`playwright.selectors.set_test_id_attribute("data-test")`), so `get_by_test_id` matches Sauce Demo's
`data-test` attributes. Don't fall back to CSS for them.

### Rules
- Define locators only in page-object constructors (`pages/*_page.py`), never in tests.
- Wrap every locator in a core element from `pages/core/` (`Input`, `Button`, `Label`, `BaseElement`, ...).
  Don't store raw `Locator` objects as page attributes. If no suitable wrapper exists, create one that inherits
  from `BaseElement`.
- Use `exact=True` when a partial name match could hit another element.
- Narrow scope by chaining from a parent instead of writing long selectors:
```python
_row = page.get_by_role("row", name="Sauce Labs Backpack")
self.btn_remove = Button(_row.get_by_role("button", name="Remove"))
```
- Pick one item from a list with `.filter(has_text=...)` or `.filter(has=...)`. Avoid `.nth()`, `.first`,
  and `.last` unless the app guarantees the order.
- Elements inside an iframe are found through `BasePage.switch_to_frame(selector)`. The page object owns the
  frame selectors (for example a dict of frame name → selector); tests pass a plain frame name, never a
  selector.
- Verify a new locator matches exactly one element (Playwright's strict mode fails otherwise). Use
  `playwright codegen` or the Inspector to confirm.

### Never use
- XPath, especially absolute XPath (`/html/body/div[2]/form/input[1]`)
- Auto-generated IDs or classes (`#input-3742`, `.css-1x9k2ab`)
- Styling or theme classes (`.btn-primary`, `.mt-4`, `.wp-block-heading`)
- Long CSS chains or positional selectors (`.parent > .child:nth-child(3)`)

---

## 5. Page Objects and the API Layer

### Page Object Model
Tests interact with the UI only through page objects, so a locator change is a single edit.

```python
# pages/login_page.py
from pages.base_page import BasePage
from pages.core.base_element import BaseElement
from pages.core.button import Button
from pages.core.input import Input
from pages.product_page import ProductPage


class LoginPage(BasePage):

    def __init__(self, page):
        """
        Initialize LoginPage and its elements.

        Args:
            page: Playwright Page used to interact with the login page.
        """
        super().__init__(page)
        self.input_username = Input(page.get_by_placeholder("Username"))
        self.input_password = Input(page.get_by_placeholder("Password"))
        self.btn_login = Button(page.get_by_role("button", name="Login"))
        self.alert_error = BaseElement(page.get_by_role("alert"))

    def submit_credentials(self, username: str, password: str):
        self.input_username.fill(username)
        self.input_password.fill(password)
        self.btn_login.click()

    def login(self, username: str, password: str) -> ProductPage:
        self.submit_credentials(username, password)
        return ProductPage(self.page)
```

- Each method has one fixed return type. Use separate methods instead of a flag that changes what is returned.
- Methods that navigate to another page return that page's object, including pages opened in a new tab or
  window (wrap the popup `Page` in its page object).
- `BasePage` and `BaseElement` already store `page` / `locator`; don't reassign them in subclasses.
- Browser dialogs (alert, confirm, prompt) go through `pages/core/dialog.py`. Handlers are registered with
  `page.once("dialog", ...)`, never `page.on(...)`: the tab is shared by every test in a file (see §6), and an
  `on` handler would stay attached and fire again in later tests ("Cannot accept dialog which is already
  handled").

### API layer
API tests talk to the service only through classes in `api/`, so an endpoint or payload change is a single
edit.

- Every API class inherits from `ApiBase` and is constructed with the request context: `XxxApi(auth.context)`
  (or `XxxApi(api_context)` for calls that must not be logged in). Never pass another API object or the
  `auth` object itself.
- Each class keeps its endpoint path in a private constant (`_CREATE_ORDER_PATH`) and exposes it through a
  method (`create_order()`), plus a method that builds the request body.
- Request bodies come from a POJO in `pojo/` (a dataclass with sensible defaults and `to_dict()` /
  `to_multipart()`) or from a JSON template in `data/` loaded with `load_payload`. Override single fields with
  keyword arguments rather than building dicts in tests.
- Send with `submit_get_api`, `submit_post_api` (`data=` for JSON, `multipart=` for file uploads),
  `submit_put_api` and `submit_delete_api`. They log every request and response. Never set `Content-Type`
  yourself; Playwright sets it, and a JSON content type breaks multipart uploads.
- Authenticate with the `auth` fixture: `auth.context`, `auth.token` (Authorization header) and
  `auth.user_id`. Log in through the fixture, not inside tests.

---

## 6. Fixtures and Test Structure

### Fixtures and the shared browser
| Fixture          | Scope    | Purpose                                                                                                                           |
|------------------|----------|-----------------------------------------------------------------------------------------------------------------------------------|
| `init_context`   | module   | Launches the `--web-browser` browser once per test file and creates one context; closes both after the file                       |
| `init_page`      | function | The one tab shared by the file's tests; resets it after each test (extra tabs closed, storage and cookies cleared, `about:blank`) |
| `login_page`     | function | The shared tab on `BASEURL`, as a `LoginPage`                                                                                     |
| `navigate_url`   | function | The shared tab on the `url` fixture; override `url` in the test class to choose the page                                          |
| `api_context`    | session  | One API request context on `APIBASEURL`                                                                                           |
| `auth`           | session  | Logs in once; `Auth(context, token, user_id)`                                                                                     |
| `create_product` | function | Creates a product and registers it for deletion after the test                                                                    |
| `delete_product` | function | List of product ids deleted after the test; skipped when the test is marked `skip_teardown`                                       |

- UI tests start from `login_page`, `navigate_url`, or a test-class fixture built on them. Never call
  `new_page()` for the test's main page; reuse the shared tab, so a file runs in one window.
- Any fixture that gives a test a page must depend on `init_page`: its teardown is the per-test reset, and
  failure screenshots look for `init_page`.
- Put repeated setup (login, adding items, navigating to a screen) in a fixture. A setup used by one file is
  a fixture in that test class; one used by several files goes in `fixtures/`.
- Data created through the API is cleaned up in fixture teardown (`create_product` / `delete_product`), not
  by the test. A test that deletes the data itself is marked `skip_teardown`.
- Teardown must not hide the test result: clean up what was created and avoid steps that can fail for
  unrelated reasons.

### Test structure
Each test follows setup → action → assert. Mark each logical step with `log_information("...")` so a failure
can be traced quickly in the log.

Every test has:
- a one-line `@pytest.mark.description("Verify ...")` marker — written to the log and the report;
- a type marker (`ui` or `api`) and one severity marker (`blocker`, `critical`, `major`, `minor`, `trivial`);
- area or kind markers where they apply (`e2e`, `dialog`, `windows`, `negative`, `smoke`, `regression`);
- a one-line docstring with the reporting-labs metadata, and nothing else in it:
  `"""@priority P1 @owner <name> @feature <area>"""`.

```python
import pytest

from config.config import APPUSERNAME, WRONGPASSWORD, LOGINERROR
from tests.base_test import BaseTest, log_information, assert_text


class TestLoginPage(BaseTest):

    @pytest.mark.description("Verify an error is shown when logging in with a wrong password.")
    @pytest.mark.ui
    @pytest.mark.negative
    @pytest.mark.major
    def test_invalid_password(self, login_page):
        """@priority P3 @owner Shantanu @feature login"""
        log_information("Log in with a wrong password")
        login_page.submit_credentials(APPUSERNAME, WRONGPASSWORD)

        log_information("Verify the error message")
        assert_text("Verify wrong credential error.", login_page.alert_error, LOGINERROR)
```

- One behavior per test; tests must not depend on each other or on run order. Within a file they share a tab,
  so a test must never rely on state left by an earlier one.
- Never keep results in module-level or `global` variables; each test builds everything it checks within its
  own run.
- Register every marker under `markers` in `pytest.ini`; `--strict-markers` makes an unregistered marker an
  error.
- Add comments only for non-obvious logic; the step logs, description and docstring cover the rest.

---

## 7. Assertions and Waits

All assertions go through `tests/base_test.py`. The assertion logic lives in the `BaseTest` class (which
inherits from `Assertion` in `utils/Assertions/assertion.py`), and the same file exposes a module-level
function for each method. Tests import and call those functions directly; they do not call the methods
through `self`. Tests never call Playwright's `expect(...)` or a bare `assert` directly. Routing everything
through one place gives every check a PASS/FAIL log line with a description, expected and actual value, and
one place to change how assertions behave. The lines themselves are written by two static methods on
`Assertion`, so every PASS and FAIL line has the same format:

| Method (on `Assertion`)                       | Logs                                                    |
|-----------------------------------------------|---------------------------------------------------------|
| `logger_info(description, expected, actual)`  | `PASS \| <description> \| Expected: ... \| Actual: ...` |
| `logger_error(description, expected, actual)` | `FAIL \| <description> \| Expected: ... \| Actual: ...` |

Assertion methods never call `logger.info` / `logger.error` with a hand-built PASS/FAIL string. Each check
logs exactly one PASS line: if a method already calls `self.assert_equal(...)` (which logs PASS through
`assert_equal_logger`), it must not call `logger_info` again.

```python
# tests/base_test.py — how each helper is exposed
def assert_equal(description, expected, actual):
    BaseTest().assert_equal(description=description, expected=expected, actual=actual)


class BaseTest(Assertion):
    def assert_equal(self, description, expected, actual):
        self.assert_equal_logger(description, expected, actual)
```

This is the project's chosen style: the module-level functions are the public API for tests, so calls read
the same in every test and in fixtures, which have no `self`. Each function creates a short-lived `BaseTest()`
to run the method; that is intentional, because the methods keep no state between calls. Reviews must not
flag module-level assertion calls or ask for `self.assert_...` instead.

### Available methods
| Function (import from `tests.base_test`)          | Use for                                                                    |
|---------------------------------------------------|----------------------------------------------------------------------------|
| `log_information(description)`                    | Logging a test step                                                        |
| `assert_equal(description, expected, actual)`     | Comparing plain values: text returned by a page method, counts, API fields |
| `assert_displayed(description, element)`          | An element becoming visible (retries)                                      |
| `assert_text(description, element, expected)`     | An element's text after an action or navigation (retries)                  |
| `assert_count(description, element, expected)`    | How many elements a locator matches, including 0 (retries)                 |
| `assert_url(description, page, expected_url)`     | The page URL after navigation (retries)                                    |
| `assert_http_ok(description, response)`           | An API response with status OK or Created                                  |

```python
# DO
from tests.base_test import assert_equal, assert_text

assert_equal("Verify item count after removal.", _count_before - 1, _count_after)
assert_text("Verify wrong credential error.", _login_page.alert_error, LOGINERROR)
```

```python
# DON'T
self.assert_equal("Verify wrong credential error.", LOGINERROR, _error_message)  # use the function
expect(_login_page.alert_error.locator).to_have_text(LOGINERROR)                 # bypasses logging
assert _error_message == LOGINERROR                                              # bypasses logging
```

### Rules
- The first argument is always a description of what is being verified, written as "Verify ...".
- Argument order is `expected`, then `actual`. Swapping them makes the failure message misleading.
- In API tests, call `assert_http_ok` before reading the body. Indexing the JSON of a failed response gives a
  confusing `KeyError` instead of the server's error.
- If the assertion you need doesn't exist, add it in two parts in `tests/base_test.py`: a method on
  `BaseTest`, and a module-level function with the same name and arguments that calls
  `BaseTest().<method>(...)`. Then add it to the table above. Never assert inline instead. Don't change
  existing methods unless the task asks for it.
- `assert_equal` compares a value at one moment and does not wait. For page state that may still be
  changing (visibility, text after an action, URL after navigation, element count), use a retrying function
  from the table, or add one that uses Playwright's `expect` internally, logging through `logger_info` and
  `logger_error`:
```python
# tests/base_test.py
from playwright.sync_api import expect

def assert_enabled(description: str, element, timeout: int = 10000):
    BaseTest().assert_enabled(description=description, element=element, timeout=timeout)


class BaseTest(Assertion):
    def assert_enabled(self, description: str, element, timeout: int = 10000):
        try:
            expect(element.locator).to_be_enabled(timeout=timeout)
            Assertion.logger_info(description, "enabled", "enabled")
        except AssertionError:
            Assertion.logger_error(description, "enabled", f"not enabled within {timeout} ms")
            raise
```
  Methods take core elements (`Input`, `Button`, `BaseElement`) or the Playwright page, not raw locators.
- Raise timeouts only for known slow operations.
- Navigate with `page.goto(url)` and then assert on an element of the target page. For pages that embed slow
  third-party content (iframes, widgets), navigate with `wait_until="domcontentloaded"`. Avoid
  `wait_until="networkidle"` — pages with analytics or polling may never go idle, making tests slow or flaky.
- Never use `page.wait_for_timeout()` or `time.sleep()`. To check a spinner or similar timed UI, assert that
  it appears and then disappears using the assertion functions from `tests.base_test`.

---

## 8. Review Checklist

When reviewing or generating code, check that:
- Files, classes, methods, and variables follow the naming table in section 2.
- Test classes inherit from `BaseTest`, have no `__init__`, and fixtures are not imported.
- No values are inlined in test methods. Settings (`config.ini`) and secrets (`.env`) come through
  `config.config`, shared structured data from `data/`, and values used by one file only are constants on
  that test class. No secret is in `config.ini`.
- Tests contain no locators; page objects wrap every locator in a core element.
- Locators follow the priority order and avoid XPath, generated or styling classes, and unfiltered indexes.
- Page methods have a single, fixed return type; navigating methods return the next page object.
- Dialog handlers use `page.once`, not `page.on`.
- UI tests get their page through `login_page`, `navigate_url` or a fixture built on them, never `new_page()`.
- API tests use API classes and the `auth` fixture, build bodies from `pojo/` or `data/`, check
  `assert_http_ok` before reading the body, and leave cleanup to fixtures (`skip_teardown` when the test
  deletes the data itself).
- No module-level or `global` variables carry state between tests.
- All assertions use the module-level functions from `tests.base_test` (not `self.assert_...`) with a
  "Verify ..." description; no direct `expect` or bare `assert` in tests, and no sleeps or fixed timeouts.
- Every test has a `description` marker, a `ui`/`api` marker, one severity marker, and the one-line
  reporting-labs docstring; all markers are registered in `pytest.ini`.
- Logical steps are marked with `log_information("...")`.
- PASS/FAIL lines go through `Assertion.logger_info` / `logger_error`, once per check.

# PytestPython – Playwright UI and API Test Automation Framework

Test automation for two applications, built with **Python**, **pytest** and **Playwright**:

- **UI tests** for [Sauce Demo](https://www.saucedemo.com) (login, products, cart, checkout) and the
  [Practice Automation](https://practice-automation.com) site (alerts, frames, new tabs and windows).
- **API tests** for the [Rahul Shetty Academy](https://rahulshettyacademy.com) e-commerce API (add product,
  create order, delete product).

The framework uses the Page Object Model with typed element wrappers, one browser per test file, a central
assertion layer that logs every check as PASS or FAIL, settings in `config.ini` with secrets kept in `.env`,
timestamped logs and HTML reports for every run, and an optional email with the report when a run finishes.

---

## Tech Stack

| Tool                                      | Purpose                                                                   |
|-------------------------------------------|---------------------------------------------------------------------------|
| Python 3.10+                              | Language (the code uses `match` statements and `str \| None` type hints)  |
| pytest                                    | Test runner, fixtures, markers, parametrization                           |
| Playwright (sync API) + pytest-playwright | Browser automation and the API request context                            |
| configparser (standard library)           | Reads the settings in `config/config.ini`                                 |
| python-dotenv                             | Loads the secrets from `.env`                                             |
| pytest-html + pytest-metadata             | Per-run HTML report with screenshots, description and test type columns   |
| reporting-labs                            | Interactive HTML and PDF report in `reporting-labs/`, emailed after a run |

---

## Project Structure

```
PytestPython/
├── .claude/skills/
│   ├── best-practice/SKILL.md      # Coding standards (applied by Claude Code automatically)
│   └── test-review/SKILL.md        # /test-review: reviews test files against the standards
├── api/                            # API request classes
│   ├── api_base.py                 # ApiBase: send + log requests, load JSON payloads from data/
│   ├── login_api.py                # LoginApi
│   ├── create_product_api.py       # CreateProductApi (multipart upload)
│   ├── create_order_api.py         # CreateOrderApi (payload from JSON or POJO)
│   └── delete_product_api.py       # DeleteProductApi
├── assets/
│   └── report.css                  # Theme for the pytest-html report
├── config/
│   ├── config.ini                  # Settings: URLs, demo users, messages, SMTP host/port (committed)
│   └── config.py                   # Reads config.ini and .env, exposes UPPERCASE constants
├── data/                           # Structured test data
│   ├── product.py                  # PRODUCTS (name, price) and CART_PRODUCT_NAMES
│   ├── create_order_api.json       # Create-order payload template
│   ├── create_product_api.json     # Create-product payload
│   └── files/T-Shirt.png           # Image uploaded by the create-product API
├── fixtures/                       # pytest plugins, registered in conftest.py
│   ├── logging_fixture.py          # Logger, per-run report/log paths, results, failure screenshots
│   ├── browser_fixture.py          # --web-browser option, init_context, init_page
│   ├── page_fixture.py             # login_page, navigate_url, url
│   ├── api_fixture.py              # api_context, auth, create_product, delete_product
│   ├── report_fixture.py           # pytest-html title, Environment table, extra columns
│   ├── retry_fixture.py            # --retries option, retries failed tests after the
│   └── email_fixture.py            # --send-email option, emails the report after the run
├── pages/                          # Page objects
│   ├── core/                       # Element wrappers: BaseElement, Input, Button, Label, Dialog
│   ├── base_page.py                # BasePage: navigate, get_url, reload, switch_to_frame, ...
│   └── <page_name>_page.py         # One page object per screen (login, product, cart, checkout, ...)
├── pojo/                           # Dataclasses that build API request bodies
│   ├── create_order.py             # CreateOrder / Order
│   └── create_product.py           # CreateProduct (to_dict, to_multipart)
├── tests/
│   ├── base_test.py                # BaseTest + log_information and assert_* functions
│   ├── api/test_<name>_api.py      # API tests
│   └── ui/test_<page_name>.py      # UI tests
├── utils/Assertions/assertion.py   # Assertion: logger_info / logger_error (PASS/FAIL lines), assert_equal_logger
├── reports/                        # Created per run: html/, log/, screenshots/
├── reporting-labs/                 # Latest reporting-labs report: index.html, report.pdf, report.json
├── .env                            # Secrets only: API login and email account (never commit)
├── conftest.py                     # Registers the fixture modules
└── pytest.ini                      # Markers, report options, console and file logging
```

---

## Setup

**1. Create and activate a virtual environment**

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows (PowerShell: .venv\Scripts\Activate.ps1)
source .venv/bin/activate       # macOS / Linux
```

**2. Install the dependencies and the browsers**

```bash
python -m pip install pytest pytest-playwright python-dotenv pytest-html pytest-metadata reporting-labs
python -m playwright install
```

**3. Check `config/config.ini`.** It holds every setting that is safe to commit: URLs and paths, the public
Sauce Demo users, expected messages and the SMTP server. Change values here, not in code:

```ini
[url]
base_url = https://www.saucedemo.com
practice_url = https://practice-automation.com

[email]
enabled = true
smtp_host = smtp.gmail.com
smtp_port = 587
```

Write values without quotes; configparser keeps quotes as part of the value. A missing section or key stops
the run at start-up with a `NoSectionError` / `NoOptionError` naming it.

**4. Create `.env`** in the project root with your own secrets:

```ini
# region API CREDENTIALS
APIUSEREMAIL=your-email@example.com
APIUSERPASSWORD=your-password
# endregion API CREDENTIALS

# region EMAIL
SMTPUSER=your-account@gmail.com
SMTPPASSWORD=your-16-letter-app-password
EMAILTO=first@example.com,second@example.com
# EMAILFROM=optional, defaults to SMTPUSER
# endregion EMAIL
```

Both files are read only through `config/config.py`, which exposes the same UPPERCASE constants
(`BASEURL`, `APPUSERNAME`, `SMTPPASSWORD`, ...) to the rest of the code. Never commit `.env`; add `.env`,
`reports/` and `reporting-labs/` to `.gitignore`.

---

## Running Tests

Run every command from the `PytestPython` folder, so pytest picks up `pytest.ini` and `conftest.py`.

| Goal                        | Command                                                                                               |
|-----------------------------|-------------------------------------------------------------------------------------------------------|
| All tests                   | `python -m pytest`                                                                                    |
| UI tests only               | `python -m pytest -m ui`                                                                              |
| API tests only              | `python -m pytest -m api`                                                                             |
| One file                    | `python -m pytest tests/ui/test_login_page.py`                                                        |
| One test                    | `python -m pytest tests/ui/test_login_page.py::TestLoginPage::test_valid_user_login`                  |
| One parametrized case       | `python -m pytest "tests/ui/test_login_page.py::TestLoginPage::test_login_shows_error[locked_user]"`  |
| By severity                 | `python -m pytest -m "blocker or critical"`                                                           |
| By name                     | `python -m pytest -k "TestProductPage and backpack"`                                                  |
| Another browser             | `python -m pytest -m ui --web-browser firefox` (`chromium` default, `firefox`, `webkit`)              |
| Email the report afterwards | `python -m pytest --send-email`                                                                       |
| Retry failed tests twice    | `python -m pytest --retries 2`                                                                        |
| No retries for this run     | `python -m pytest --retries 0`                                                                        |

### Markers

Every marker is registered in `pytest.ini`; `--strict-markers` turns a misspelled marker into an error.

| Group    | Markers                                                    | Meaning                                         |
|----------|------------------------------------------------------------|-------------------------------------------------|
| Type     | `ui`, `api`                                                | Which layer the test exercises                  |
| Area     | `e2e`, `dialog`, `windows`                                 | End-to-end flows, browser dialogs, tabs/windows |
| Kind     | `negative`, `smoke`, `regression`                          | Negative scenarios, smoke and regression suites |
| Severity | `blocker`, `critical`, `major`, `minor`, `trivial`         | Impact if the test fails                        |
| Info     | `description("Verify ...")`                                | One-line summary, shown in the log and report   |
| Cleanup  | `skip_teardown`                                            | Keep API data the test created (no cleanup)     |

---

## Test Coverage

38 test runs: 33 UI and 5 API.

| Test file                        | Tests | What it verifies                                                                       |
|----------------------------------|-------|----------------------------------------------------------------------------------------|
| `ui/test_login_page.py`          | 3     | Valid login reaches Products; locked-out user and wrong password show the right error  |
| `ui/test_product_page.py`        | 16    | Price and Add to cart button for all 6 products, empty cart, cart badge, Remove button |
| `ui/test_cart_page.py`           | 1     | Cart lists the products that were added                                                |
| `ui/test_e2e_scenario_page.py`   | 4     | Full checkout to "Thank you for your order!", and the 3 checkout validation errors     |
| `ui/test_alert_page.py`          | 5     | Alert, confirm (accept and dismiss) and prompt (with and without a name) dialogs       |
| `ui/test_frame_page.py`          | 2     | Docs page header inside each of the two iframes                                        |
| `ui/test_window_page.py`         | 2     | Heading in the page opened by New Tab and by New Window                                |
| `api/test_add_product_api.py`    | 1     | A logged-in user can add a product (multipart upload)                                  |
| `api/test_create_order_api.py`   | 3     | Order from the JSON payload, from the POJO, and with two products                      |
| `api/test_delete_product_api.py` | 1     | A product can be deleted by its creator                                                |

---

## How the Framework Works

### Browser lifecycle: one browser per test file

| Fixture        | Scope    | What it does                                                                                                                                                                       |
|----------------|----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `init_context` | module   | Launches the browser chosen with `--web-browser` once per test file and creates one context. Closes both after the file's last test.                                               |
| `init_page`    | function | Gives every test the same tab. After each test it closes extra tabs, clears localStorage, sessionStorage and cookies, and returns to `about:blank`, so the next test starts clean. |

Each test file therefore opens one browser window, all its tests run in that window, and it closes at the
end of the file. Chromium starts maximized (`--start-maximized` with `no_viewport=True`); Firefox and WebKit
use a 1280×720 viewport. Sauce Demo uses `data-test` attributes, so the fixture sets them as the test-id
attribute and page objects can use `get_by_test_id(...)`.

Because the tab is shared, dialog handlers must be one-time: `Dialog.accept_next()` and `dismiss_next()`
register with `page.once("dialog", ...)`, never `page.on(...)`.

### Fixtures

Fixture modules are registered in `conftest.py` through `pytest_plugins`; tests never import them.

| Fixture               | Scope    | Provides                                                                        |
|-----------------------|----------|---------------------------------------------------------------------------------|
| `login_page`          | function | The shared tab on `BASEURL`, as a `LoginPage`                                   |
| `navigate_url`        | function | The shared tab on `url` (wait until DOM content loaded), as a Playwright `Page` |
| `url`                 | function | Default `PRACTICEURL`; override it in a test class to open another page         |
| `api_context`         | session  | One Playwright request context on `APIBASEURL` for the whole run                |
| `auth`                | session  | Logs in once; an `Auth` object with `context`, `token` and `user_id`            |
| `create_product`      | function | Creates a product and returns its id; the product is deleted after the test     |
| `delete_product`      | function | A list of product ids to delete after the test (skipped with `skip_teardown`)   |
| `log_test_boundaries` | autouse  | Logs START, the description and END of every test                               |

Overriding `url` for one test file:

```python
class TestAlertPage(BaseTest):

    @pytest.fixture
    def url(self):
        return f"{PRACTICEURL}{POPUPSPATH}"
```

### Page objects and element wrappers

Every locator lives in a page-object constructor and is wrapped in a typed element, so each element only
offers actions that make sense for it.

```
BaseElement   is_displayed, is_visible, get_text, get_attribute, get_count, click, focus, press, screenshot
 ├── Input    fill, clear, get_value, select_text, is_editable
 ├── Button   click, double_click
 └── Label    get_label_text
Dialog        accept_next(text), dismiss_next()   (browser alert / confirm / prompt)
```

Page objects inherit from `BasePage` (`navigate`, `get_url`, `reload`, `go_back`, `go_forward`,
`switch_to_frame`). Methods that move to another screen return that screen's page object, for example
`LoginPage.login(...)` returns a `ProductPage`. Item-specific lookups on `ProductPage` first find the product
card by its exact name and then search inside it, so `get_item_price("Sauce Labs Backpack")` can never
return another product's price.

### API layer

```
ApiBase              submit_get_api, submit_post_api, submit_put_api, submit_delete_api, load_payload
 ├── LoginApi        login(), login_api_payload()
 ├── CreateProductApi create_product(), create_product_api_payload(**overrides)   (multipart)
 ├── CreateOrderApi  create_order(), create_order_api_payload_json(id), create_order_api_payload_pojo(ids)
 └── DeleteProductApi delete_product_path(id)
```

Request bodies come from a POJO in `pojo/` (a dataclass with defaults you can override) or from a JSON
template in `data/`. Every request and response is logged. API tests use `auth` for the request context,
token and user id:

```python
_order_api = CreateOrderApi(auth.context)
_response = _order_api.submit_post_api(url=_order_api.create_order(),
                                       data=_order_api.create_order_api_payload_pojo([create_product]),
                                       headers={"Authorization": auth.token})
```

### Assertions

Tests import the assertion functions from `tests/base_test.py`. Each one logs a `PASS` or `FAIL` line with
the description, expected and actual value, written by `Assertion.logger_info` and `Assertion.logger_error`
in `utils/Assertions/assertion.py` so every line has the same format. The retrying ones use Playwright's
`expect`, so they wait for the page to settle.

| Function                                       | Use for                                       |
|------------------------------------------------|-----------------------------------------------|
| `log_information(description)`                 | A test step in the log                        |
| `assert_equal(description, expected, actual)`  | Plain values: text, numbers, API fields       |
| `assert_text(description, element, expected)`  | An element's text (retries)                   |
| `assert_displayed(description, element)`       | An element becoming visible (retries)         |
| `assert_count(description, element, expected)` | How many elements a locator matches (retries) |
| `assert_url(description, page, expected_url)`  | The page URL (retries)                        |
| `assert_http_ok(description, response)`        | An API response with status OK or Created     |

### Logs, reports and screenshots

Each run writes to its own timestamped folder:

```
reports/2026-10-17_20-30-05/
├── html/report2026-10-17_20-30-05.html   # pytest-html report, self-contained
├── log/test_run2026-10-17_20-30-05.log   # full DEBUG log of the run
└── screenshots/                          # one PNG per open tab for each failed UI test
```

The HTML report shows the Environment (base URLs, browser, test type), a Description column from the
`description` marker and a Test Type column (UI or API). Failure screenshots are also embedded in the report.

reporting-labs writes the latest interactive report and its PDF to `reporting-labs/`. It reads the test
priority, owner and feature from a one-line docstring on each test:

```python
def test_valid_user_login(self, login_page):
    """@priority P1 @owner Shantanu @feature login"""
```

A sample of the console log:

```
20:30:05 | INFO  | ========== START: test_valid_user_login ==========
20:30:05 | INFO  | Description: Verify a valid user lands on the home page after logging in.
20:30:05 | INFO  | Login with Valid username and password
20:30:06 | INFO  | PASS | Verify home page heading. | Expected: Products | Actual: Products
20:30:06 | INFO  | RESULT: PASSED | test_valid_user_login | 1.12s
20:30:06 | INFO  | ========== END: test_valid_user_login ==========
```

### Emailing the report

After the run, `fixtures/email_fixture.py` can email the reporting-labs report (PDF and HTML attached) with a
summary table of passed, failed, errors and skipped.

- Send for one run: `python -m pytest --send-email`.
- Send after every run: set `enabled = true` under `[email]` in `config/config.ini` (`false` sends only
  with `--send-email`).
- Several recipients: separate them with commas in `EMAILTO`.
- Gmail needs an **app password**, not the account password: turn on 2-Step Verification, create one at
  [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords) and paste the 16 letters,
  without spaces, into `SMTPPASSWORD`.
- A failed send is logged as `Report email not sent | <reason>` and never changes the test result.

### Retrying failed tests

`fixtures/retry_fixture.py` retries failed tests **after the whole run**, not immediately, and keeps their
original order. With 10 tests where test 4 fails, the order is 1, 2, 3, 4, 5 … 10, then 4 again.

| Setting                   | Where                                                                   |
|---------------------------|-------------------------------------------------------------------------|
| Default number of retries | `retries` under `[execution]` in `config/config.ini` (`0` turns it off) |
| For one run               | `python -m pytest --retries N`                                          |
| In CI                     | `PYTEST_ADDOPTS="--retries 2"`                                          |

- While retries are left, a failure is reported as **RERUN** (`R` in the console) instead of FAILED. It is
  still logged and screenshotted.
- After the last test, a `RETRY ROUND n` block in the log lists the tests being retried.
- A test that passes on retry counts as passed; one that fails its last retry counts as **FAILED**.
- Before each retry round every fixture is torn down, so retried tests get a fresh browser and a fresh API
  login.
- The pytest-html report shows first attempts under **Reruns**, and the report email adds a **Reruns** row.

A test that keeps showing up as RERUN is flaky. The final result may be green, but it is worth investigating.

---

## Writing a New Test

**UI test**

1. **Page object**: add `pages/<page_name>_page.py` with a class inheriting from `BasePage`. Wrap every
   locator in an element type and name it with a type prefix (`input_`, `btn_`, `lbl_`, `lnk_`, `alert_`).
2. **Data**: values used by one file are UPPERCASE constants on the test class; shared settings go in
   `config/config.ini` (exposed through `config/config.py`), secrets in `.env`, structured data in `data/`.
3. **Test**: add `tests/ui/test_<page_name>.py`:

```python
import pytest

from config.config import APPUSERNAME, PASSWORD
from data.product import CART_PRODUCT_NAMES
from tests.base_test import BaseTest, log_information, assert_count


class TestCartPage(BaseTest):

    @pytest.mark.description("Verify the cart item count after adding products.")
    @pytest.mark.ui
    @pytest.mark.major
    def test_verify_cart_count(self, login_page):
        """@priority P3 @owner Shantanu @feature cart"""
        log_information("Login with Valid username and password")
        _product_page = login_page.login(APPUSERNAME, PASSWORD)

        log_information("Add the products to the cart")
        for _product_name in CART_PRODUCT_NAMES:
            _product_page.click_add_to_cart(_product_name)
        _cart_page = _product_page.click_on_cart()

        log_information("Verify the items in the cart")
        assert_count("Verify that items count in cart", _cart_page.cart_quantity, len(CART_PRODUCT_NAMES))
```

   Every test gets a `description` marker, `ui` or `api`, one severity marker, and the one-line
   reporting-labs docstring.

**API test**

1. Add an API class in `api/` that inherits from `ApiBase`, with the endpoint path and a payload method.
2. Build the body from a POJO in `pojo/` or a JSON template in `data/`.
3. In the test, use `auth` for the context and token, and `create_product` / `delete_product` for any data
   that must be cleaned up.

Conventions: files `test_<page_name>.py`, classes `Test<PageName>(BaseTest)`, methods `test_<behaviour>`,
local variables prefixed with `_`, no locators or hardcoded values in tests, and no `time.sleep()` or
`wait_for_timeout()`. The full standard is in `.claude/skills/best-practice/SKILL.md`.

---

## Claude Code Skills

- **best-practices**: the project's coding standards (layout, naming, data, locators, page objects,
  fixtures, API layer, assertions, waits). Claude Code applies it automatically when writing or changing code.
- **test-review**: reviews test files against those standards. Run `/test-review` for all tests, or
  `/test-review tests/ui/test_login_page.py` for one file.

---

## Notes

- Browsers run headed with `slow_mo=300` (set in `fixtures/browser_fixture.py`). Switch to headless for CI
  machines without a display.
- Tests within a file share one tab, which is reset after every test. If a test passes on its own but fails
  in a full file run, check for state the reset doesn't cover.
- API products created by `create_product` are deleted after each test; mark a test `skip_teardown` when it
  deletes the product itself.
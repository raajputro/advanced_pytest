# XYZ Bank – BDD Web Automation (Python + Playwright + pytest-bdd + POM)

End-to-end deposit flow on the public demo bank
**GlobalSQA XYZ Bank** → https://www.globalsqa.com/angularJs-protractor/BankingProject/

| # | Requirement | Where it happens |
|---|-------------|------------------|
| 1 | Demo banking website | `config/settings.py` → `BASE_URL` |
| 2 | Login | `CustomerLoginPage.login_as()` |
| 3 | Find account & check balance | `AccountPage.select_account()` / `get_balance()` |
| 4 | Deposit an amount | `AccountPage.deposit()` |
| 5 | Verify balance updated | `AccountPage.expect_balance(before + amount)` |
| 6 | Screenshot | `BasePage.take_screenshot()` → `screenshots/` (+ embedded in HTML report) |
| 7 | Logout | `AccountPage.logout()` |

## Project structure
```
xyz-bank-bdd/
├── config/settings.py            # URL, timeouts, paths (env-overridable)
├── features/
│   └── banking_deposit.feature   # Gherkin scenario outline (data-driven)
├── pages/                        # Page Object Model
│   ├── base_page.py              # open, screenshot, shared helpers
│   ├── home_page.py              # Customer / Manager login choice
│   ├── customer_login_page.py    # "Your Name" dropdown + Login
│   └── account_page.py           # account select, balance, deposit, logout
├── tests/step_defs/
│   └── test_banking_deposit.py   # pytest-bdd step definitions
├── mock_site/index.html          # offline replica of XYZ Bank (optional)
├── conftest.py                   # fixtures, --mock-site option, report hooks
├── pytest.ini
└── requirements.txt
```

## Setup (Windows PowerShell)
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
playwright install chromium
```

## Run
```powershell
pytest                                  # live GlobalSQA site, headless
pytest --headed --slowmo 500            # watch it run
pytest -m smoke                         # by tag
pytest -k "Harry"                       # one example row
pytest --browser firefox                # other browsers
pytest --mock-site                      # offline replica (if the live site is down)
pytest --count=20                       # repeat every scenario 20 times
pytest --count=20 -n 4                  # ...across 4 parallel browsers
pytest --count=20 -x                    # stop at the first failure
```
Outputs:
- `screenshots/` – step-6 screenshots (timestamped)
- `reports/report.html` – self-contained HTML report with screenshots embedded
- `reports/artifacts/` – Playwright auto-screenshot on failure

## Add more test data
Just add rows to the `Examples:` table in the feature file. Valid customers/accounts on the demo site:

| Customer | Accounts |
|---|---|
| Hermoine Granger | 1001, 1002, 1003 |
| Harry Potter | 1004, 1005, 1006 |
| Ron Weasly | 1007, 1008, 1009 |
| Albus Dumbledore | 1010, 1011, 1012 |
| Neville Longbottom | 1013, 1014, 1015 |

## Notes
- The balance check is **relative** (`before + amount`), so it stays green regardless of prior state.
  The demo site resets its data on page reload.
- `--mock-site` serves `mock_site/index.html` locally. It mirrors the live site's selectors
  (`#userSelect`, `#accountSelect`, `ng-click`, `ng-model`, `.logout`) so the same page objects work on both.

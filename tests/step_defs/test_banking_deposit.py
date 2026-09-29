from pytest_bdd import given, parsers, scenarios, then, when

from pages.account_page import AccountPage
from pages.customer_login_page import CustomerLoginPage
from pages.home_page import HomePage

scenarios("banking_deposit.feature")  # resolved via bdd_features_base_dir in pytest.ini


# ---------------- Given ----------------
@given("the customer is on the XYZ Bank home page")
def open_home(page, app_url):
    home = HomePage(page)
    home.open(app_url)
    home.is_loaded()


# ---------------- When ----------------
@when(parsers.parse('the customer logs in as "{customer}"'))
def login(page, customer, ctx):
    HomePage(page).go_to_customer_login()
    login_page = CustomerLoginPage(page)
    login_page.is_loaded()
    login_page.login_as(customer)
    AccountPage(page).is_loaded_for(customer)
    ctx["customer"] = customer


@when(parsers.parse('the customer selects account "{account}"'))
def select_account(page, account, ctx):
    AccountPage(page).select_account(account)
    ctx["account"] = account


@when(parsers.parse('the customer deposits "{amount:d}"'))
def deposit(page, amount):
    AccountPage(page).deposit(amount)


@when("the customer logs out")
def logout(page):
    AccountPage(page).logout()


# ---------------- Then ----------------
@then("the current balance of the account is recorded")
def record_balance(page, ctx):
    account_page = AccountPage(page)
    assert account_page.get_account_number() == ctx["account"]
    ctx["balance_before"] = account_page.get_balance()
    print(f"\n[info] {ctx['customer']} / {ctx['account']} balance before: {ctx['balance_before']}")


@then(parsers.parse('the message "{message}" is displayed'))
def verify_message(page, message):
    actual = AccountPage(page).get_message()
    assert actual == message, f"Expected '{message}', got '{actual}'"


@then(parsers.parse('the balance is increased by "{amount:d}"'))
def verify_balance(page, amount, ctx):
    account_page = AccountPage(page)
    expected = ctx["balance_before"] + amount
    account_page.expect_balance(expected)  # auto-waits for the Angular binding
    ctx["balance_after"] = account_page.get_balance()
    print(f"[info] balance after: {ctx['balance_after']} (expected {expected})")


@then(parsers.parse('a screenshot named "{name}" is taken'))
def screenshot(page, name, ctx):
    path = AccountPage(page).take_screenshot(name)
    ctx.setdefault("screenshots", []).append(path)
    assert path.exists() and path.stat().st_size > 0
    print(f"[info] screenshot saved: {path}")


@then("the customer login screen is displayed")
def verify_logged_out(page):
    CustomerLoginPage(page).is_loaded()

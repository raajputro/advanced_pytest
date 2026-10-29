from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class AccountPage(BasePage):
    """Customer dashboard: account selector, balance, deposit form, logout."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.welcome_name = page.locator("span.fontBig")
        self.account_select = page.locator("#accountSelect")
        # "Account Number : 1004 , Balance : 0 , Currency : Dollar" -> three <strong> tags
        self.account_info = page.locator("div.center strong")
        self.deposit_tab = page.locator("button[ng-click='deposit()']")
        self.amount_input = page.locator("input[ng-model='amount']")
        self.deposit_submit = page.locator("form button[type='submit']", has_text="Deposit")
        self.message = page.locator("span.error")
        self.logout_btn = page.locator("button.logout")

    # ---------- checks ----------
    def is_loaded_for(self, customer_name: str) -> None:
        expect(self.welcome_name).to_have_text(customer_name)

    # ---------- account ----------
    def select_account(self, account_number: str) -> None:
        self.account_select.select_option(label=account_number)
        expect(self.account_info.nth(0)).to_have_text(account_number)

    def get_account_number(self) -> str:
        return self.account_info.nth(0).inner_text().strip()

    def get_balance(self) -> int:
        return int(self.account_info.nth(1).inner_text().strip())

    def expect_balance(self, expected: int) -> None:
        expect(self.account_info.nth(1)).to_have_text(str(expected))

    # ---------- deposit ----------
    def deposit(self, amount: int) -> None:
        self.deposit_tab.click()
        expect(self.amount_input).to_be_visible()
        self.amount_input.fill(str(amount))
        self.deposit_submit.click()

    def get_message(self) -> str:
        expect(self.message).to_be_visible()
        return self.message.inner_text().strip()

    # ---------- session ----------
    def logout(self) -> None:
        self.logout_btn.click()

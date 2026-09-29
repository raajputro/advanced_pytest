from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class CustomerLoginPage(BasePage):
    """'Your Name' dropdown + Login button."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.user_select = page.locator("#userSelect")
        self.login_btn = page.locator("button[type='submit']", has_text="Login")

    def is_loaded(self) -> None:
        expect(self.user_select).to_be_visible()

    def login_as(self, customer_name: str) -> None:
        self.user_select.select_option(label=customer_name)
        expect(self.login_btn).to_be_visible()
        self.login_btn.click()

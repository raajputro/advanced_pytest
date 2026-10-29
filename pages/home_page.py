from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class HomePage(BasePage):
    """Landing page: choose Customer or Bank Manager login."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.customer_login_btn = page.locator("button[ng-click='customer()']")
        self.manager_login_btn = page.locator("button[ng-click='manager()']")

    def is_loaded(self) -> None:
        expect(self.customer_login_btn).to_be_visible()

    def go_to_customer_login(self) -> None:
        self.customer_login_btn.click()

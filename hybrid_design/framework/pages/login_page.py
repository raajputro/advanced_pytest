from playwright.async_api import expect
from .base_page import BasePage


class LoginPage(BasePage):
    async def open_login(self):
        await self.open()

    async def submit(self, username: str, password: str):
        await self.page.locator("#user-name").fill(username)
        await self.page.locator("#password").fill(password)
        await self.page.locator("#login-button").click()

    async def expect_error(self, message: str):
        await expect(self.page.locator('[data-test="error"]')).to_contain_text(message)

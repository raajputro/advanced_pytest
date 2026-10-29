from playwright.async_api import expect
from .base_page import BasePage


class CartPage(BasePage):
    async def expect_backpack(self):
        backpack = self.page.locator(
            '[data-test="cart-list"] [data-test="inventory-item-name"]'
        )
        await expect(backpack).to_have_text("Sauce Labs Backpack")

    async def checkout(self):
        await self.page.locator('[data-test="checkout"]').click()

    async def remove_backpack(self):
        await self.page.locator('[data-test="remove-sauce-labs-backpack"]').click()

    async def expect_empty(self):
        await expect(self.page.locator('[data-test="inventory-item"]')).to_have_count(0)

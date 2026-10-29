from playwright.async_api import expect
from .base_page import BasePage


class InventoryPage(BasePage):
    async def expect_loaded(self):
        await expect(self.page).to_have_url(f"{self.base_url}/inventory.html")
        await expect(self.page.locator('[data-test="title"]')).to_have_text("Products")

    async def add_backpack(self):
        await self.page.locator('[data-test="add-to-cart-sauce-labs-backpack"]').click()

    async def open_cart(self):
        await self.page.locator('[data-test="shopping-cart-link"]').click()

    async def expect_cart_count(self, count: int):
        badge = self.page.locator('[data-test="shopping-cart-badge"]')
        if count == 0:
            await expect(badge).to_have_count(0)
        else:
            await expect(badge).to_have_text(str(count))

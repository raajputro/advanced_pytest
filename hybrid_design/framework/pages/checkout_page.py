from playwright.async_api import expect
from .base_page import BasePage
from framework.builders.customer_builder import Customer


class CheckoutPage(BasePage):
    async def enter_customer(self, customer: Customer):
        await self.page.locator('[data-test="firstName"]').fill(customer.first_name)
        await self.page.locator('[data-test="lastName"]').fill(customer.last_name)
        await self.page.locator('[data-test="postalCode"]').fill(customer.postal_code)

    async def continue_to_overview(self):
        await self.page.locator('[data-test="continue"]').click()

    async def expect_error(self, message: str):
        await expect(self.page.locator('[data-test="error"]')).to_contain_text(message)

    async def finish(self):
        await self.page.locator('[data-test="finish"]').click()

    async def expect_complete(self):
        await expect(self.page.locator('[data-test="complete-header"]')).to_have_text("Thank you for your order!")

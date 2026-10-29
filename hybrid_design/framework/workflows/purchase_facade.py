"""Facade: orchestrates pages but leaves individual assertions visible to tests."""
from framework.builders.customer_builder import Customer
from framework.pages.login_page import LoginPage
from framework.pages.inventory_page import InventoryPage
from framework.pages.cart_page import CartPage
from framework.pages.checkout_page import CheckoutPage
from framework.strategies.login_strategy import LoginStrategy


class PurchaseFacade:
    def __init__(self, login: LoginPage, inventory: InventoryPage,
                 cart: CartPage, checkout: CheckoutPage):
        self.login, self.inventory = login, inventory
        self.cart, self.checkout = cart, checkout

    async def add_backpack_to_cart(self, auth: LoginStrategy):
        await self.login.open_login()
        await auth.authenticate(self.login)
        await self.inventory.expect_loaded()
        await self.inventory.add_backpack()
        await self.inventory.open_cart()

    async def purchase_backpack(self, auth: LoginStrategy, customer: Customer):
        await self.add_backpack_to_cart(auth)
        await self.cart.expect_backpack()
        await self.cart.checkout()
        await self.checkout.enter_customer(customer)
        await self.checkout.continue_to_overview()
        await self.checkout.finish()

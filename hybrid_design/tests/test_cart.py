import pytest
from framework.strategies.login_strategy import StandardLogin


@pytest.mark.regression
async def test_add_backpack(purchase, cart_page):
    await purchase.add_backpack_to_cart(StandardLogin())
    await cart_page.expect_backpack()


@pytest.mark.regression
async def test_remove_backpack(purchase, cart_page):
    await purchase.add_backpack_to_cart(StandardLogin())
    await cart_page.remove_backpack()
    await cart_page.expect_empty()


@pytest.mark.regression
async def test_cart_badge(inventory_page, login_page):
    await login_page.open_login()
    await StandardLogin().authenticate(login_page)
    await inventory_page.add_backpack()
    await inventory_page.expect_cart_count(1)

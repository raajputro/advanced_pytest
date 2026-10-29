import pytest
from framework.builders.customer_builder import CustomerBuilder
from framework.strategies.login_strategy import StandardLogin


@pytest.mark.smoke
async def test_purchase_end_to_end(purchase, checkout_page):
    customer = CustomerBuilder().with_name("Rahim", "Ahmed").with_postal_code("1212").build()
    await purchase.purchase_backpack(StandardLogin(), customer)
    await checkout_page.expect_complete()


@pytest.mark.negative
@pytest.mark.parametrize("first,last,zip_code,error", [
    ("", "Ahmed", "1212", "First Name is required"),
    ("Rahim", "", "1212", "Last Name is required"),
    ("Rahim", "Ahmed", "", "Postal Code is required"),
])
async def test_checkout_required_fields(purchase, cart_page, checkout_page,
                                        first, last, zip_code, error):
    await purchase.add_backpack_to_cart(StandardLogin())
    await cart_page.checkout()
    customer = CustomerBuilder().with_name(first, last).with_postal_code(zip_code).build()
    await checkout_page.enter_customer(customer)
    await checkout_page.continue_to_overview()
    await checkout_page.expect_error(error)

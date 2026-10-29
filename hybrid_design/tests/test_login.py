import pytest
from framework.strategies.login_strategy import StandardLogin, LockedOutLogin


@pytest.mark.smoke
async def test_standard_login(login_page, inventory_page):
    await login_page.open_login()
    await StandardLogin().authenticate(login_page)
    await inventory_page.expect_loaded()


@pytest.mark.negative
async def test_locked_out_login(login_page):
    await login_page.open_login()
    await LockedOutLogin().authenticate(login_page)
    await login_page.expect_error("Sorry, this user has been locked out")


@pytest.mark.negative
@pytest.mark.parametrize("username,password,error", [
    ("", "secret_sauce", "Username is required"),
    ("standard_user", "", "Password is required"),
    ("invalid_user", "invalid_password", "Username and password do not match"),
])
async def test_login_validation(login_page, username, password, error):
    await login_page.open_login()
    await login_page.submit(username, password)
    await login_page.expect_error(error)

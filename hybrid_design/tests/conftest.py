"""Dependency injection via fixtures. Each test owns an isolated browser context."""
import os
from pathlib import Path

import pytest
import pytest_asyncio
from playwright.async_api import async_playwright

from framework.config import Settings
from framework.factories.browser_factory import BrowserFactory
from framework.pages.login_page import LoginPage
from framework.pages.inventory_page import InventoryPage
from framework.pages.cart_page import CartPage
from framework.pages.checkout_page import CheckoutPage
from framework.workflows.purchase_facade import PurchaseFacade


def pytest_addoption(parser):
    group = parser.getgroup("hybrid framework")
    group.addoption("--base-url", default=os.getenv("BASE_URL", "https://www.saucedemo.com"))
    group.addoption("--browser-name", choices=["chromium", "firefox", "webkit"], default=os.getenv("BROWSER", "chromium"))
    group.addoption("--headed", action="store_true", help="Launch a visible browser")
    group.addoption("--slow-mo", type=int, default=0)
    group.addoption("--timeout-ms", type=int, default=10000)


@pytest.fixture(scope="session")
def settings(pytestconfig):
    return Settings(
        base_url=pytestconfig.getoption("--base-url"),
        browser=pytestconfig.getoption("--browser-name"),
        headless=not pytestconfig.getoption("--headed"),
        slow_mo=pytestconfig.getoption("--slow-mo"),
        timeout_ms=pytestconfig.getoption("--timeout-ms"),
    )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


@pytest_asyncio.fixture
async def page(request, settings):
    async with async_playwright() as playwright:
        browser = await BrowserFactory.create(
            playwright, settings.browser,
            headless=settings.headless, slow_mo=settings.slow_mo,
        )
        context = await browser.new_context()
        page = await context.new_page()
        page.set_default_timeout(settings.timeout_ms)
        try:
            yield page
        finally:
            if getattr(request.node, "rep_call", None) and request.node.rep_call.failed:
                out = Path("artifacts/screenshots")
                out.mkdir(parents=True, exist_ok=True)
                # Safe for parametrized tests and parallel xdist workers.
                import re
                from uuid import uuid4
                test_name = re.sub(r"[^a-zA-Z0-9_-]", "_", request.node.nodeid)
                try:
                    await page.screenshot(path=str(out / f"{test_name}_{uuid4().hex[:8]}.png"), full_page=True)
                except Exception as exc:
                    print(f"Screenshot unavailable: {exc}")
            await context.close()
            await browser.close()


@pytest.fixture
def login_page(page, settings):
    return LoginPage(page, settings.base_url)


@pytest.fixture
def inventory_page(page, settings):
    return InventoryPage(page, settings.base_url)


@pytest.fixture
def cart_page(page, settings):
    return CartPage(page, settings.base_url)


@pytest.fixture
def checkout_page(page, settings):
    return CheckoutPage(page, settings.base_url)


@pytest.fixture
def purchase(login_page, inventory_page, cart_page, checkout_page):
    return PurchaseFacade(login_page, inventory_page, cart_page, checkout_page)

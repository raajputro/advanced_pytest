"""Factory: choose browser implementation without branching in tests."""
from playwright.async_api import Playwright, Browser


class BrowserFactory:
    @staticmethod
    async def create(playwright: Playwright, name: str, *, headless: bool, slow_mo: int) -> Browser:
        browsers = {
            "chromium": playwright.chromium,
            "firefox": playwright.firefox,
            "webkit": playwright.webkit,
        }
        if name not in browsers:
            raise ValueError(f"Unsupported browser {name!r}; choose from {list(browsers)}")
        return await browsers[name].launch(headless=headless, slow_mo=slow_mo)

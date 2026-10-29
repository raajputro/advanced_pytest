from datetime import datetime
from pathlib import Path
from uuid import uuid4

from playwright.sync_api import Page, expect

from config.settings import DEFAULT_TIMEOUT_MS, SCREENSHOT_DIR


class BasePage:
    """Common behaviour shared by every page object."""

    def __init__(self, page: Page):
        self.page = page
        self.page.set_default_timeout(DEFAULT_TIMEOUT_MS)

    def open(self, url: str) -> None:
        self.page.goto(url, wait_until="domcontentloaded")

    def take_screenshot(self, name: str) -> Path:
        SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
        safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in name)
        path = SCREENSHOT_DIR / f"{safe}_{datetime.now():%Y%m%d_%H%M%S_%f}_{uuid4().hex[:6]}.png"
        self.page.screenshot(path=str(path), full_page=True)
        return path

    def expect_url_contains(self, fragment: str) -> None:
        expect(self.page).to_have_url(f"**{fragment}**")

from playwright.async_api import Page


class BasePage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url.rstrip("/")

    async def open(self, path: str = "") -> None:
        await self.page.goto(f"{self.base_url}/{path.lstrip('/')}")

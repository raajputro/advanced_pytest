import re
from playwright.sync_api import Page, expect

def test_has_title(page: Page):
    page.goto("https://erpstaging.brac.net")

    # Expect a title "to contain" a substring.
    expect(page).to_have_title(re.compile("Sign in to BRAC ERP"))

    page.get_by_role("input", name="username").fill("testuser")
    page.get_by_role("input", name="password").fill("testpassword")
    page.get_by_role("button", name="Sign In").click()

    expect(page).to_have_url(re.compile("dashboard"))

# def test_get_started_link(page: Page):
#     page.goto("https://playwright.dev/")

#     # Click the get started link.
#     page.get_by_role("link", name="Get started").click()

#     # Expects page to have a heading with the name of Installation.
#     expect(page.get_by_role("heading", name="Installation")).to_be_visible()
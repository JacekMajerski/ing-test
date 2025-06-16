import pytest
from playwright.sync_api import sync_playwright, TimeoutError
from pages.cookie_settings_page import CookieSettingsPage

@pytest.mark.parametrize("browser_name", ["chromium", "firefox", "webkit"])
def test_accept_analytics_cookie(browser_name):
    with sync_playwright() as p:
        browser = getattr(p, browser_name).launch()
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://www.ing.pl")
        page.wait_for_load_state("networkidle")

        cookie_settings = CookieSettingsPage(page)

        try:
            cookie_settings.open_custom_settings()
        except TimeoutError as e:
            page.screenshot(path=f"error_screenshot_{browser_name}.png", full_page=True)
            with open(f"error_dom_{browser_name}.html", "w", encoding="utf-8") as f:
                f.write(page.content())
            raise e

        cookie_settings.accept_analytics_and_confirm()

        cookies = page.context.cookies()
        policy_cookie = next((c for c in cookies if c["name"] == "cookiePolicyGDPR"), None)
        assert policy_cookie is not None, "Brak ciasteczka 'cookiePolicyGDPR'."
        assert policy_cookie["value"] == "3", f"Oczekiwano 'cookiePolicyGDPR' z wartością '3', otrzymano: {policy_cookie['value']}"

        browser.close()

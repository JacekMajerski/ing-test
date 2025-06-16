import pytest
from playwright.sync_api import expect, TimeoutError, sync_playwright
from pages.cookie_settings_page import CookieSettingsPage

def test_accep(page):
    page.goto("https://www.pracuj.pl/")
    expect(page.locator('[data-test="button-submitCookie"]')).to_be_visible(timeout=60000)


# def test_accept_analytics_cookie(page):
#     page.goto("https://www.ing.pl", timeout=60000)
#
#     print("TITLE:", page.title())
#     print("URL:", page.url)
#
#     page.screenshot(path="error_screenshot.png", full_page=True)
#     with open("error_dom.html", "w", encoding="utf-8") as f:
#         f.write(f"<h1>{page.title()}</h1><p>{page.url}</p>")
#         f.write(page.content())
#
#     expect(page.locator("#login-desktop")).to_be_visible(timeout=60000)
#
#     cookie_settings = CookieSettingsPage(page)
#
#     try:
#         cookie_settings.open_custom_settings()
#     except TimeoutError as e:
#         page.screenshot(path="error_screenshot.png", full_page=True)
#         with open("error_dom.html", "w", encoding="utf-8") as f:
#             f.write(page.content())
#         raise e
#
#     cookie_settings.accept_analytics_and_confirm()
#
#     cookies = page.context.cookies()
#     policy_cookie = next((c for c in cookies if c["name"] == "cookiePolicyGDPR"), None)
#     assert policy_cookie is not None, "Brak ciasteczka 'cookiePolicyGDPR'."
#     assert policy_cookie["value"] == "3", f"Oczekiwano 'cookiePolicyGDPR' z wartością '3', otrzymano: {policy_cookie['value']}"


def test_anty_antybot():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            locale="pl-PL"
        )
        page = context.new_page()
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        page.goto("https://www.ing.pl", timeout=60000)

        # "Ludzkie" zachowanie
        page.mouse.move(100, 100)
        page.wait_for_timeout(1000)
        page.mouse.move(150, 200)
        page.wait_for_timeout(1000)

        page.screenshot(path="antybot_screenshot.png", full_page=True)
        print("Tytuł strony:", page.title())
        cookie_settings = CookieSettingsPage(page)
        cookie_settings.open_custom_settings()


        context.close()
        browser.close()

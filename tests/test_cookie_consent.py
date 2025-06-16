import pytest
from playwright.sync_api import expect, TimeoutError
from pages.cookie_settings_page import CookieSettingsPage
def test_accep(page):
    page.goto("https://www.pracuj.pl/")
    expect(page.locator('[data-test="button-submitCookie"]')).to_be_visible(timeout=60000)


def test_debug_ing_home(page):
    page.goto("https://www.ing.pl")
    page.wait_for_load_state("load", timeout=60000)
    print("Tytuł strony:", page.title())
    body_text = page.locator("body").inner_text()
    print("BODY TEXT:", body_text[:500])
    assert "cookie" in body_text.lower() or "logowanie" in body_text.lower()

def test_accept_analytics_cookie(page):
    page.goto("https://www.ing.pl")
    page.wait_for_load_state("load", timeout=60000)
    print("TITLE:", page.title())
    print("URL:", page.url)
    page.screenshot(path="error_screenshot.png", full_page=True)
    with open("error_dom.html", "w", encoding="utf-8") as f:
        f.write(f"<h1>{page.title()}</h1><p>{page.url}</p>")
        f.write(page.content())

    expect(page.locator("#login-desktop")).to_be_visible(timeout=60000)

    # Inicjalizacja strony obsługi ciasteczek
    cookie_settings = CookieSettingsPage(page)

    try:
        cookie_settings.open_custom_settings()
    except TimeoutError as e:
        # W razie błędu zrób screenshot i zapisz DOM
        page.screenshot(path="error_screenshot.png", full_page=True)
        with open("error_dom.html", "w", encoding="utf-8") as f:
            f.write(page.content())
        raise e

    # Akceptacja ciasteczek analitycznych
    cookie_settings.accept_analytics_and_confirm()

    # Pobierz ciasteczka i sprawdź
    cookies = page.context.cookies()
    policy_cookie = next((c for c in cookies if c["name"] == "cookiePolicyGDPR"), None)
    assert policy_cookie is not None, "Brak ciasteczka 'cookiePolicyGDPR'."
    assert policy_cookie["value"] == "3", f"Oczekiwano 'cookiePolicyGDPR' z wartością '3', otrzymano: {policy_cookie['value']}"
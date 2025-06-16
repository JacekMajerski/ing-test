import pytest
from playwright.sync_api import expect, TimeoutError
from pages.cookie_settings_page import CookieSettingsPage

def test_accept_analytics_cookie(page):
    page.goto("https://www.ing.pl")
    page.wait_for_load_state("networkidle", timeout=60000)

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
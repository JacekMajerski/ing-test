import pytest
from playwright.sync_api import expect, TimeoutError, sync_playwright
from pages.cookie_settings_page import CookieSettingsPage
import random, requests

def get_poland_proxies():
    url = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&country=PL&timeout=5000&anonymity=elite"
    resp = requests.get(url, timeout=10)
    return [p.strip() for p in resp.text.splitlines() if p.strip()]

def test_anty_antybot_with_proxy(page, browser_name):
    # Wybierz losowe PL proxy, jeśli dostępne
    proxies = get_poland_proxies()
    proxy = random.choice(proxies) if proxies else None

    # Otwórz nowy browser/context z proxy
    browser = page.context.browser
    browser.launch(
        headless=False,
        proxy={"server": f"http://{proxy}"} if proxy else None
    )
    page.goto("https://www.ing.pl", timeout=60000)
    page.wait_for_timeout(5000)

    # Maskowanie ruchów myszy
    page.mouse.move(100, 100)
    page.wait_for_timeout(1000 + random.randint(0, 200))
    page.mouse.move(200, 300)
    page.wait_for_timeout(1000 + random.randint(0, 500))

    expect(page.get_by_role("button", name="Dostosuj")).to_be_visible(timeout=60000)
    CookieSettingsPage(page).open_custom_settings()

@pytest.mark.usefixtures("page")
def test_accep(page):
    page.goto("https://www.pracuj.pl/")
    expect(page.locator('[data-test="button-submitCookie"]')).to_be_visible(timeout=60000)

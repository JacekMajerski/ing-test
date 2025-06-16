from playwright.sync_api import sync_playwright, expect
from pages.cookie_settings_page import CookieSettingsPage
import random, requests

def get_poland_proxies():
    url = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&country=PL&timeout=5000&anonymity=elite"
    resp = requests.get(url, timeout=10)
    return [p.strip() for p in resp.text.splitlines() if p.strip()]

def test_anty_antybot_with_proxy():
    proxies = get_poland_proxies()
    proxy = random.choice(proxies) if proxies else None

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            proxy={"server": f"http://{proxy}"} if proxy else None,
        )
        context = browser.new_context(
            viewport={"width": 1366, "height": 768},
            locale="pl-PL",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
            timezone_id="Europe/Warsaw",
            geolocation={"longitude": 21.0, "latitude": 52.2},
            permissions=["geolocation"],
        )

        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get:()=>undefined});
            Object.defineProperty(navigator, 'plugins', {get:()=>[1,2,3]});
            Object.defineProperty(navigator, 'languages', {get:()=>['pl-PL','pl']});
        """)

        page = context.new_page()
        page.goto("https://www.ing.pl", timeout=60000)
        page.wait_for_timeout(5000)
        page.mouse.move(100, 100)
        page.mouse.move(300, 200)
        expect(page.get_by_role("button", name="Dostosuj")).to_be_visible(timeout=10000)
        CookieSettingsPage(page).open_custom_settings()

        browser.close()

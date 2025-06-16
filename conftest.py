import pytest
from playwright.sync_api import sync_playwright

def pytest_addoption(parser):
    parser.addoption("--mybrowser", action="store", default="chromium", help="Przeglądarka: chromium, firefox, webkit")
    parser.addoption("--isheaded", action="store", default="false", help="Tryb headed: true/false")

@pytest.fixture(scope="session")
def browser_name(pytestconfig):
    return pytestconfig.getoption("--mybrowser")

@pytest.fixture(scope="session")
def headed_mode(pytestconfig):
    return pytestconfig.getoption("--isheaded").lower() == "true"

@pytest.fixture
def page(browser_name, headed_mode):
    with sync_playwright() as p:
        browser = getattr(p, browser_name).launch(headless=not headed_mode)

        context = browser.new_context(
            viewport={"width": 1360, "height": 800},
            ignore_https_errors=True,
            locale="pl-PL",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
            geolocation={"longitude": 21.0, "latitude": 52.2},
            permissions=["geolocation"]
        )

        context.clear_cookies()
        context.clear_permissions()

        page = context.new_page()
        yield page
        context.close()
        browser.close()

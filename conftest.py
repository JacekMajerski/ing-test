import pytest
from playwright.sync_api import sync_playwright

def pytest_addoption(parser):
    parser.addoption("--mybrowser", action="store", default="chromium", help="Przeglądarka: chromium, firefox, webkit")
    parser.addoption("--isheaded", action="store", default="false", help="Tryb headed: true/false")  # zmiana tutaj

@pytest.fixture(scope="session")
def browser_name(pytestconfig):
    return pytestconfig.getoption("--mybrowser")

@pytest.fixture(scope="session")
def headed_mode(pytestconfig):
    return pytestconfig.getoption("--isheaded").lower() == "true"  # zmiana tutaj

@pytest.fixture
def page(browser_name, headed_mode):
    with sync_playwright() as p:
        browser = getattr(p, browser_name).launch(headless=not headed_mode)
        context = browser.new_context()
        page = context.new_page()
        yield page
        context.close()
        browser.close()

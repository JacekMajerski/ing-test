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
        # Uruchom przeglądarkę
        browser = getattr(p, browser_name).launch(headless=not headed_mode)

        # Utwórz incognito (czysty) kontekst
        context = browser.new_context(
            viewport={"width": 1360, "height": 800},
            ignore_https_errors=True,
        )

        # Dodatkowo - wyczyść dane (opcjonalnie, ale bezpieczne)
        context.clear_cookies()
        context.clear_permissions()

        # Nowa strona w kontekście
        page = context.new_page()
        yield page

        # Zamknij kontekst i przeglądarkę po teście
        context.close()
        browser.close()

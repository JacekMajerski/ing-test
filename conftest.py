import pytest
from playwright.sync_api import sync_playwright

def pytest_addoption(parser):
    parser.addoption("--mybrowser", action="store", default="chromium")
    parser.addoption("--isheaded", action="store", default="false")

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
            viewport={"width": 1366, "height": 768},
            locale="pl-PL",
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            geolocation={"longitude": 21.0, "latitude": 52.2},
            permissions=["geolocation"],
            timezone_id="Europe/Warsaw",
            has_touch=False,  # nie udawaj dotyku
            is_mobile=False
        )

        context.clear_cookies()
        context.clear_permissions()

        page = context.new_page()

        page.add_init_script("""
            // Ukryj webdriver
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });

            // Dodaj fałszywe wtyczki
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });

            // Dodaj języki
            Object.defineProperty(navigator, 'languages', {
                get: () => ['pl-PL', 'pl'],
            });

            // Dodaj "chrome" jako właściwość
            window.navigator.chrome = {
                runtime: {},
                // Fałszywy user-agent klienta
                app: 'Chrome',
                webstore: {}
            };

            // Ukryj właściwość `navigator.connection.rtt` i inne
            Object.defineProperty(navigator, 'connection', {
                get: () => ({
                    downlink: 10,
                    effectiveType: '4g',
                    rtt: 50,
                    saveData: false,
                })
            });

            // Ukryj `permissions.query` wykrywalne po headless
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) =>
                parameters.name === 'notifications'
                    ? Promise.resolve({ state: Notification.permission })
                    : originalQuery(parameters);

            // Fałszywe screen i window właściwości
            Object.defineProperty(window, 'outerHeight', { get: () => window.innerHeight + 88 });
            Object.defineProperty(window, 'outerWidth', { get: () => window.innerWidth });

            // Blokuj debuggery antybotowe (np. Selenium detect)
            window.__selenium_unwrapped = true;
            window.document.__webdriver_script_fn = true;

            // Ukryj DevTools detection (czeka, czy debugger aktywny)
            const originalDebug = console.debug;
            console.debug = (...args) => {
                if (args.length === 1 && typeof args[0] === 'string' && args[0].includes('Selenium')) {
                    return;
                }
                return originalDebug(...args);
            };
        """)

        yield page
        context.close()
        browser.close()

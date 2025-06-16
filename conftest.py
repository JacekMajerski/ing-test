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
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)…",
            timezone_id="Europe/Warsaw",
            geolocation={"longitude":21.0,"latitude":52.2},
            permissions=["geolocation"],
            has_touch=False,
            is_mobile=False
        )
        context.clear_cookies()
        context.clear_permissions()

        page = context.new_page()
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get:()=>undefined});
            Object.defineProperty(navigator, 'plugins', {get:()=>[1,2,3,4,5]});
            Object.defineProperty(navigator, 'languages', {get:()=>['pl-PL','pl']});
            window.navigator.chrome={runtime:{},app:'Chrome',webstore:{}};
            Object.defineProperty(navigator,'connection',{get:()=>({downlink:10,effectiveType:'4g',rtt:50,saveData:false})});
            const origQ=window.navigator.permissions.query;
            window.navigator.permissions.query = params => params.name==='notifications'?Promise.resolve({state: Notification.permission}):origQ(params);
            Object.defineProperty(navigator,'hardwareConcurrency',{get:()=>4});
            Object.defineProperty(navigator,'deviceMemory',{get:()=>8});
        """)

        yield page
        context.close()
        browser.close()

import pytest
import os
from dotenv import load_dotenv  # do ładowania zmiennych środowiskowych z pliku .env
from playwright.sync_api import sync_playwright  # główna biblioteka Playwright dla testów synchronicznych
import logging
from colorlog import ColoredFormatter  # kolorowe logowanie w konsoli

# 🔧 Konfiguracja kolorowego logowania
formatter = ColoredFormatter(
    "%(log_color)s%(levelname)s: %(message)s",  # Format logu: kolor + poziom logu + wiadomość
    log_colors={
        'DEBUG':    'cyan',
        'INFO':     'green',
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL': 'bold_red',
    }
)

# 🔧 Ustawienie handlera do wypisywania logów na standardowe wyjście (konsola)
handler = logging.StreamHandler()
handler.setFormatter(formatter)

# 🔧 Skonfigurowanie głównego loggera
logger = logging.getLogger()
logger.setLevel(logging.INFO)  # tylko logi INFO i wyżej będą widoczne
logger.handlers = [handler]   # używamy tylko tego jednego handlera (żeby uniknąć duplikatów)

# 📦 Wczytanie zmiennych środowiskowych z pliku .env (np. BASE_URL)
load_dotenv()

# 🌐 Fixture: bazowy URL testowanej aplikacji (czytany z .env lub domyślnie podany)
@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL", "https://default.url")  # domyślny URL jeśli brak w .env

# 🧪 Dodanie własnych opcji do linii komend pytesta
def pytest_addoption(parser):
    parser.addoption("--mybrowser", action="store", default="chromium", help="Przeglądarka: chromium, firefox, webkit")
    parser.addoption("--isheaded", action="store", default="false", help="Tryb headed: true/false")

# 📌 Fixture: przeglądarka wybrana z linii komend (domyślnie chromium)
@pytest.fixture(scope="session")
def browser_name(pytestconfig):
    return pytestconfig.getoption("--mybrowser")

# 📌 Fixture: tryb wyświetlania (czy testy mają być uruchamiane w trybie graficznym)
@pytest.fixture(scope="session")
def headed_mode(pytestconfig):
    return pytestconfig.getoption("--isheaded").lower() == "true"

# 📄 Fixture: główny obiekt strony dla testów
@pytest.fixture
def page(browser_name, headed_mode):
    # 🔄 Uruchomienie kontekstu Playwrighta
    with sync_playwright() as p:
        # 🚀 Start przeglądarki w trybie graficznym lub headless
        browser = getattr(p, browser_name).launch(headless=not headed_mode)

        # 🧼 Tworzenie nowego kontekstu (jak nowy profil przeglądarki)
        context = browser.new_context(
            viewport={"width": 1280, "height": 800},  # standardowy rozmiar okna
            ignore_https_errors=True,  # ignoruj błędy HTTPS (np. certyfikaty lokalne)
        )

        # 🧹 Wyczyść cookies i uprawnienia — opcjonalne, ale bezpieczne dla czystych testów
        context.clear_cookies()
        context.clear_permissions()

        # 📄 Otwórz nową stronę w tym kontekście
        page = context.new_page()
        yield page  # przekazanie obiektu page do testu

        # 🧨 Po teście: zamknij kontekst i przeglądarkę
        context.close()
        browser.close()

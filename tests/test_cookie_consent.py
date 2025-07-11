import pytest
import logging
from playwright.sync_api import Page, expect
from pages.cookie_settings_page import CookieSettingsPage


def test_accept_analytics_cookie(page: Page, base_url: str):
    #hop na strone główną ING
    page.goto(base_url)

    # Zainicjalizuj obiekt strony do obsługi ustawień ciasteczek (Page Object)
    cookie_settings = CookieSettingsPage(page)

    # Kliknij przycisk „Dostosuj” w banerze cookies
    cookie_settings.open_custom_settings()

    # Zaznacz checkbox „Analityczne” i kliknij „Zaakceptuj zaznaczone”
    cookie_settings.accept_analytics_and_confirm()

    # Pobierz wszystkie ciasteczka z bieżącego kontekstu przeglądarki
    cookies = page.context.cookies()

    # Znajdź ciasteczko odpowiedzialne za zgodę na ciasteczka – cookiePolicyGDPR
    policy_cookie = next((cookie for cookie in cookies if cookie["name"] == "cookiePolicyGDPR"), None)

    # Sprawdź, czy ciasteczko zostało ustawione
    assert policy_cookie is not None, "Brak ciasteczka 'cookiePolicyGDPR'."

    # Sprawdź, czy wartość ciasteczka oznacza akceptację analitycznych (3 = zgody analityczne)
    assert policy_cookie["value"] == "3", f"Oczekiwano 'cookiePolicyGDPR' z wartością '3', otrzymano: {policy_cookie['value']}"

    # Jesli asercja skonczyla sie sukcesem - wyloguj komunikat
    logging.info(f'Ustawiono prawidłową wartość ciasteczka: {policy_cookie["value"]}')
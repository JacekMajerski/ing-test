# ING Cookie Consent Test

Automatyczny test Playwright + pytest do weryfikacji zachowania ciasteczek na stronie https://www.ing.pl

## 🔧 Instalacja

```bash
pip install -r requirements.txt
playwright install
```

## 🚀 Uruchomienie testu lokalnie

```bash
pytest tests/test_cookie_consent.py
```

## ✅ Co testujemy?

1. Wejście na stronę ing.pl
2. Kliknięcie „Dostosuj”
3. Wybranie zgody na ciasteczka analityczne
4. Kliknięcie „Zaakceptuj wybrane”
5. Weryfikacja, że odpowiednie ciasteczka zostały zapisane

## 🎁 Bonus: CI z testem w wielu przeglądarkach

W `.github/workflows/playwright.yml` zawarty jest pipeline GitHub Actions, który uruchamia testy w przeglądarkach Chromium, Firefox i WebKit.

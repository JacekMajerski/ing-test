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
## 🧪 Uruchomienie testów we wszystkich przeglądarkach

W systemie Windows możesz użyć gotowego skryptu `run_all_browsers.bat`, który uruchamia testy w Chromium, Firefox i WebKit:

```bash
run_all_browsers.bat
```

## ✅ Co testujemy?

1. Wejście na stronę ing.pl
2. Kliknięcie „Dostosuj”
3. Wybranie zgody na ciasteczka analityczne
4. Kliknięcie „Zaakceptuj wybrane”
5. Weryfikacja, że odpowiednie ciasteczka zostały zapisane

## 🎁 Bonus: CI z testem w wielu przeglądarkach

W `.github/workflows/playwright.yml` zawarty jest pipeline GitHub Actions, który uruchamia testy w przeglądarkach Chromium, Firefox i WebKit. Jest też obsługa artefaktów, niestety testy nie działają - najprawdopodobniej należałoby ustawić jakieś odpowiednie proxy. Przykładowy run wraz z raportami, gdzie na próbę dodałem test innej domeny można znaleźć na https://github.com/JacekMajerski/ing-test/actions/runs/15707602420

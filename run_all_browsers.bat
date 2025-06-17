@echo off
setlocal

set BROWSERS=chromium firefox webkit

if not exist reports mkdir reports

::Zostana wykonane wszystkie testy z katalogu tests. Testy zostana nadpisane
for %%B in (%BROWSERS%) do (
    echo Uruchamianie testów w %%B...
    start /B cmd /c pytest tests/ --mybrowser=%%B --isheaded=false --html=reports/report_%%B.html --self-contained-html
)

:: Czekaj na zakończenie testów (przybliżony czas – można dostosować)
timeout /T 120 >nul

echo Wszystkie testy zakończone. Raporty znajdziesz w folderze reports\.

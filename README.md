<div align="center">

# Adam Bielas

**Full Stack Developer · Tychy, Polska**

Tworzę aplikacje i integracje, które rozwiązują konkretne problemy w codziennej pracy.

[Zobacz moje portfolio](https://rabuuwu.github.io/) · [GitHub](https://github.com/Rabuuwu) · [LinkedIn](https://www.linkedin.com/in/adambielas/)

</div>

---

## Cześć, tu Adam

Na co dzień rozwijam i administruję produkcyjnym CRM u operatora internetu i telewizji. Lubię pracę blisko procesu: od rozmowy o potrzebie, przez model danych i interfejs, po wdrożenie, utrzymanie i wsparcie użytkowników.

Wcześniej pracowałem jako monter telekomunikacyjny. To doświadczenie nadal pomaga mi patrzeć na oprogramowanie szerzej niż tylko przez kod — liczą się też urządzenia, adresy, ludzie i sposób, w jaki naprawdę wykonują swoją pracę.

## Co pokazuję

W portfolio zebrałem wybrane realizacje komercyjne i projekty, które rozwijam po godzinach. Opisuję w nich problem, swój udział i efekt, zamiast sprowadzać całość do listy technologii.

- **CRM i procesy firmowe** — między innymi obieg magazynowy, integracje, KSeF oraz podsumowania rozmów tworzone z użyciem lokalnego modelu AI.
- **D&D Companion** — aplikacja, w której rozwijam karty postaci, kampanie, ekwipunek i notatki do sesji RPG.
- **TradingHelper** — narzędzie do analizy rynku i symulacji PAPER z aplikacją desktopową na macOS i Windows. Na macOS lokalny OCR automatycznie odczytuje widoczne ceny TradingView; OCR nie działa na Windowsie.
- **FSE-IT** — eksperyment, który oddzielam od ukończonych i używanych realizacji.

Najczęściej pracuję z Node.js, TypeScriptem, Reactem i PostgreSQL. Dobieram narzędzia do zadania; ważniejsze od samego stosu jest dla mnie to, czy rozwiązanie da się wdrożyć, utrzymać i wygodnie rozwijać.

## Zajrzyj na stronę

Portfolio jest po polsku i angielsku. Możesz tam przełączyć motyw, otworzyć opisy projektów i zobaczyć mój profil zawodowy.

**[rabuuwu.github.io](https://rabuuwu.github.io/)**

## Testy przeglądarkowe

Uruchom lokalny serwer poleceniem opisanym wyżej, zainstaluj Playwright i jego Chromium, a następnie w drugim terminalu wykonaj:

```bash
python3 -m playwright install chromium
python3 tests/browser_check.py
python3 tests/case_studies_check.py
```

Domyślnie testy używają Chromium zarządzanego przez Playwright, a zrzuty zapisują poza repozytorium w katalogu tymczasowym. Możesz ustawić `CHROME_PATH` lub `PORTFOLIO_ARTIFACT_DIR`, aby jawnie wskazać przeglądarkę albo miejsce artefaktów.

Jeśli chcesz porozmawiać o aplikacji, integracji albo stronie internetowej, [napisz do mnie](mailto:adam.bielas.praca@gmail.com).

---

Stronę zbudowałem w HTML, CSS i JavaScript. Lokalny podgląd uruchomisz poleceniem `python3 -m http.server 8765 --bind 127.0.0.1` w katalogu projektu, a następnie otworzysz `http://127.0.0.1:8765`.

## Lokalna kontrola jakości

Treści PL/EN mają źródło w `content/portfolio.json`, układ w `templates/home.html`, a wygenerowane HTML są zapisane w repozytorium. Po zmianie treści wykonaj:

```bash
python3 scripts/build_portfolio.py
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Osiem testów sprawdza odtwarzalność czternastu stron, linki/fragmenty i zasoby, metadane oraz uczciwe rozdzielenie stażu IT od stanowiska programisty. Osobne testy przeglądarkowe nadal są potrzebne do oceny motywów, języków, klawiatury i responsywności. CI weryfikuje PR; publikacja pozostaje osobnym krokiem istniejącego workflow na `main`.

Sekcje Engineering i AI & Automation rozdzielają obecne rozwiązania, ograniczenia oraz prace w rozwoju. Poprawki audytowe powstały przy wsparciu Codexa; ich obecność nie dowodzi samodzielnego opanowania wszystkich mechanizmów przez autora. Nie deklarujemy wyników wydajności bez odtwarzalnych pomiarów. Istniejące PDF CV wymagają osobnego przeglądu przed aktualizacją i publikacją.

## SEO i wersje językowe

Angielska strona główna jest dostępna pod `/`, a polska pod `/pl/`. Case studies mają osobne ścieżki w `/projects/<slug>/` i `/pl/projects/<slug>/`. Generator buduje statyczne metadane, canonical, `hreflang`, Open Graph i dane JSON-LD dla każdej wersji. `sitemap.xml` zawiera strony główne oraz case studies w obu językach; `robots.txt` wskazuje sitemapę. Workflow Pages publikuje te pliki razem z obiema wersjami witryny.

Po publikacji dodaj domenę do Google Search Console i Bing Webmaster Tools, prześlij `https://rabuuwu.github.io/sitemap.xml` i sprawdź raport indeksowania oraz wybrane zapytania. Sam plik sitemap nie potwierdza indeksacji.

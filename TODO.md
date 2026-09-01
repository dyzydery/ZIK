# TODO :
## Koszyk:
- [ ] Loty sa zepsute, na razie markujemy 0.0 zeby nie zepsuc CSV
- [ ] Średnia jajka
- [ ] Średnia kurczaka
- [ ] cinemacity
- [ ] wiecej sklepow
- [x] otomoto - automatycznie rok-3
- [ ] najtansze jablka

## Indeks
- [x] Indeks Złotego
- [ ] Koszyk inflacyjny
- [ ] Różnice w czasie
- [ ] Inflancja Y2Y

## Side projekciki
- [ ] Loty - kiedy najlepiej kupic - zaczac od 6 miesiac
- [x] Kindle

## Reseach
- [ ] Strona internetowa

## Bugi - krytyczne
- [ ] `-1` jako sentinel zatruwa wszystko: w bazie ma byc `NULL`, nie `-1`
- [ ] `inflacja.py:28` obsluguje tylko `stare < 0`, nie obsluguje `nowe < 0` -> kazdy zepsuty scraper wchodzi do sredniej jako -100% deflacji
- [ ] `prad` = `0.0` (nie `-1`) -> `ZeroDivisionError` w `inflacja.py:32`
- [ ] `try/except` w `calculateInflation` obejmuje CALA petle -> jeden wyjatek przerywa liczenie reszty i zostawia zera, ktore potem wchodza do `statistics.mean`. Ma byc try per pozycja
- [ ] `DBgetNotNullValue` bierze ostatnia dodatnia wartosc z dowolnej daty -> "inflacja Y2Y" nie jest Y2Y (stad chleb 4836%)
- [ ] `skrobaczka.py:121` - `if (url.find('chleb')):` jest ZAWSZE prawdziwe (`find` zwraca -1 = truthy). Ma byc `if 'chleb' in url:`
- [ ] `skrobaczka.py:228` - `benzyna()` jedyny scraper bez `try/except`, wywala caly nocny run
- [ ] Brak `timeout=` we wszystkich `requests.get` -> cron moze zawisnac na zawsze
- [x] `waluty()` - klucz juz w `.env` (OK), zostaje reszta: brak obslugi `success: false` -> przy limicie API leci `KeyError` i caly run pada bez zapisania wiersza; `http` zamiast `https` (sprawdzone, https dziala); klejenie klucza w f-stringu zamiast `params=` (klucz wpada do URL-a w logach i tracebackach)
- [ ] `skrobaczka.py:32` - nagi `raise` bez aktywnego wyjatku (dziala przypadkiem)
- [ ] Wyciac cookies sesyjne z 2021 z `fryzjer()` (`skrobaczka.py:146` i `:152`) - `permuserid`, `_ga`, `_fbp` w publicznym repo
- [ ] Polaczenia sqlite nigdy nie zamykane (`baza.py`) - zamykane sa tylko kursory
- [ ] `kindle.py:28` wola `zrobCene(x)` z 1 argumentem, sygnatura to `zrobCene(item, x)` - plik martwy

## Rozjazd danych
- [ ] `ceny` 1028 wierszy / `zik` 1021 / CSV 1024 - trzy niezalezne zapisy, juz sie rozjechaly
- [ ] `DBinsert` - jedna transakcja na obie tabele zamiast dwoch osobnych commitow
- [ ] CSV generowac Z BAZY, nie dopisywac rownolegle
- [ ] Tabela `zik` zapisuje `-1/xau` jako pozornie legalna wartosc

## Scrapery do naprawy (stan sprawdzony 2026-08-31)
- [ ] `bigmac` - Uber Eats zwraca 404 / anti-bot challenge, zrodlo do wymiany
- [ ] `piwo` - URL `pid,3192` redirectuje na `pid,153955`, produkt zmienil ID, tylko zaktualizowac `koszyk.py`
- [ ] `aspiryna` - redirect na `/produkt/aspirin-10-tabl,3795`, stary URL
- [ ] `fryzjer` - API `/api/salon-prices/M58` nie istnieje, redirect na strone glowna
- [ ] `jajka` - strona ma tylko cene `0`, produkt niedostepny we Frisco, znalezc inny
- [ ] `lot` - SPA, cena tylko z JS (3.5 kB HTML), trzeba API Ryanaira
- [ ] `kasjer` - sciana consent/JS, 975 B tresci
- [ ] `auto`, `m2wtorny`, `m2pierwotny`, `upc`, `prad` - strona wraca 200 z pelna trescia, tylko selektory nie pasuja
- [ ] `auto` i `m2` opieraja sie na hashowanych klasach CSS (`efpuxbr16 ooa-1n2paoq er34gjf0`, `data-v-0d6d0a35`) - to sie zmienia przy kazdym deployu strony. Przepisac na JSON-LD / `__NEXT_DATA__` / `data-testid`
- [ ] `aspiryna()` i `frisco()` robia 2x request na ta sama strone - rozdzielic "pobierz strone" od "wyciagnij cene"

## Architektura
- [ ] Lista kolumn zduplikowana w 5 miejscach: `baza.py:15`, `baza.py:22`, `baza.py:25`, `inflacja.py:24`, `plot.py:52` + derywacja w `funkcyjki.saveCSV`
- [ ] UWAGA: `saveCSV` bierze kolejnosc z `koszyk.koszyk` - wstawienie nowej pozycji W SRODKU listy przesunie kolumny CSV wzgledem historycznych wierszy, bez ostrzezenia
- [ ] `koszyk.py` jako jedyne zrodlo definicji (nazwa, opis, URL, parser, ile kolumn), INSERT/nazwy/wykresy generowane z tego
- [ ] `requirements.txt` (requests, bs4, pandas, seaborn, matplotlib, python-dotenv)
- [ ] `.env.example` jest nietrackowany - dodac do repo, zeby bylo wiadomo jakie zmienne sa potrzebne
- [x] Cron nie czyta `.bashrc` - sprawdzic, czy `FIXER_API_KEY` faktycznie dociera do runu na Mikrusie (`load_dotenv()` czyta `.env` z CWD, wiec w crontabie musi byc `cd` do katalogu projektu)

## Jakosc danych
- [ ] Walidacja wiarygodnosci ceny - zmiana >30% wzgledem ostatniej dodatniej wartosci = flaga do przegladu. Dzis kazda sparsowana liczba wchodzi jako prawda (`mydlo` skacze 39.90 -> 45.90 -> 48.90 za kostke mydla, cos podmienilo produkt)
- [ ] Opis w `koszyk.py` rozjechany z URL-em: `mydlo` (Bialy Jelen 150g vs "barwa mydlo szare"), `kindle` (8gb vs URL 16gb), `telefon` (1TB vs 256GB)
- [ ] Raport zdrowia scraperow po kazdym runie - lista pozycji z `-1` + ile dni w takim stanie. 13 z 33 pozycji lezy od >60 dni i nikt tego nie zauwazyl
- [ ] Tabela zmian produktu `(produkt, data_od, opis, url)` + pionowa kreska na wykresie w miejscu podmiany - kluczowe dla indeksu 100-letniego

## Waluty
- [ ] fixer.io zwraca XAU z 6 miejscami po przecinku (`0.00026`) - jeden krok kwantyzacji to ~0.4% ceny zlota (~70 zl na uncji). Caly indeks jest skwantowany co 0.4%, widac w bazie skoki 17046 -> 17302 -> 17128
- [ ] Zbierac rownolegle NBP `api.nbp.pl/api/cenyzlota` (cena 1g zlota, za darmo, bez klucza, historia od 2013) w nowej kolumnie - nie tracac ciaglosci szeregu

## Repo
- [x] `lazygit` - 21 MB binarki w gicie, do `.gitignore`
- [x] `zik.db` commitowany codziennie (588 kB pelnego snapshotu dziennie) - wystarczy CSV, baze odtwarzac z CSV
- [ ] `TODO` (bez rozszerzenia) - starsza kopia tego pliku, do usuniecia
- [ ] `test.py` to demo kolorow ANSI, nie test - kolory zduplikowane z `funkcyjki.py`
- [ ] `funkcyjki.znajdzSrednia` - martwy kod, jest `statistics.mean`
- [ ] Miks tabow (`skrobaczka.py`) i 4 spacji (reszta)
- [ ] `wykresuj()` zakomentowane w `zik.py:83` - wykresy w README sa z 2025-10-24
- [x] Pilnowac, zeby debugowy stan `zik.py` (`WyliczZIK()` zakomentowane, aktywne `printPage`) nie wjechal na master

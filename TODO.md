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
- [x] `prad` = `0.0` -> naprawione 2026-09-03: scraper zwraca 0.97 (laczny koszt 1 kWh), historyczne 500 wierszy cofniete do `-1` w `ceny`, `zik` i CSV
- [ ] `try/except` w `calculateInflation` obejmuje CALA petle -> jeden wyjatek przerywa liczenie reszty i zostawia zera, ktore potem wchodza do `statistics.mean`. Ma byc try per pozycja
- [ ] `DBgetNotNullValue` bierze ostatnia dodatnia wartosc z dowolnej daty -> "inflacja Y2Y" nie jest Y2Y (stad chleb 4836%)
- [ ] `skrobaczka.py:121` - `if (url.find('chleb')):` jest ZAWSZE prawdziwe (`find` zwraca -1 = truthy). Ma byc `if 'chleb' in url:`
- [ ] `skrobaczka.py:228` - `benzyna()` jedyny scraper bez `try/except`, wywala caly nocny run
- [ ] Brak `timeout=` we WSZYSTKICH 9 wywolaniach `requests.get` (sprawdzone 2026-09-03: `grep -c timeout` = 0) -> cron moze zawisnac bez konca. Bez tego `except requests.RequestException` jest martwym kodem, bo wyjatek nigdy nie powstanie
- [ ] `waluty()` - zrobione: klucz w `.env`, `from None`. NIE zrobione: `timeout`, cztery bramki awarii (cofnely sie, patrz Regresje), oraz `http` zamiast `https` (sprawdzone 2026-09-03: nadal `http://data.fixer.io`, a https na tym kluczu dziala)
- [ ] `skrobaczka.py:32` - nagi `raise` bez aktywnego wyjatku (dziala przypadkiem)
- [ ] Wyciac cookies sesyjne z 2021 z `fryzjer()` (`skrobaczka.py:146` i `:152`) - `permuserid`, `_ga`, `_fbp` w publicznym repo
- [ ] Polaczenia sqlite nigdy nie zamykane (`baza.py`) - zamykane sa tylko kursory
- [ ] `kindle.py:28` wola `zrobCene(x)` z 1 argumentem, sygnatura to `zrobCene(item, x)` - plik martwy

## Rozjazd danych
- [ ] `ceny` 1034 / `zik` 1027 / CSV 1030 (stan 2026-09-03) - trzy niezalezne zapisy, rozjazd staly: 7 i 4 wiersze
- [ ] Pogodzic zbiory: 3 wiersze z 2020 istnieja TYLKO w CSV, 7 wierszy z 2021 TYLKO w bazie. Zaden plik nie jest nadzbiorem - regeneracja CSV z bazy skasowalaby te 3
- [ ] `DBinsert` - jedna transakcja na obie tabele zamiast dwoch osobnych commitow
- [ ] CSV generowac Z BAZY, nie dopisywac rownolegle
- [ ] Tabela `zik` zapisuje `-1/xau` jako pozornie legalna wartosc

## Scrapery do naprawy (stan sprawdzony 2026-08-31)
- [ ] `bigmac` - stary naglowek `{'accept':'text/html'}` dostaje 403 od Cloudflare ("Just a moment..."). ZRODLO JEST OK, nie trzeba wymieniac - cena 24.70 zl potwierdzona recznie 2026-08-31, ciaglosc szeregu (2020: 11.30 -> 2024: 22.90 -> 2025-10: 23.70) da sie utrzymac
- [ ] `piwo` - URL `pid,3192` redirectuje na `pid,153955`, produkt zmienil ID, tylko zaktualizowac `koszyk.py`
- [ ] `aspiryna` - redirect na `/produkt/aspirin-10-tabl,3795`, stary URL
- [ ] `fryzjer` - API `/api/salon-prices/M58` nie istnieje, redirect na strone glowna
- [ ] `jajka` - strona ma tylko cene `0`, produkt niedostepny we Frisco, znalezc inny
- [ ] `lot` - SPA, cena tylko z JS (3.5 kB HTML), trzeba API Ryanaira
- [ ] `auto`, `m2wtorny`, `m2pierwotny` - strona wraca 200 z pelna trescia, tylko selektory nie pasuja
- [ ] `upc` - NIE selektor: 493 kB HTML ale tylko 1577 znakow tekstu, tresc renderowana JS-em
- [ ] `kasjer` - NIE selektor: 987 B HTML, 74 znaki tekstu, sciana bot/consent
- [ ] `auto` i `m2` opieraja sie na hashowanych klasach CSS (`efpuxbr16 ooa-1n2paoq er34gjf0`, `data-v-0d6d0a35`) - to sie zmienia przy kazdym deployu strony. Przepisac na JSON-LD / `__NEXT_DATA__` / `data-testid`
- [ ] `aspiryna()` i `frisco()` robia 2x request na ta sama strone - rozdzielic "pobierz strone" od "wyciagnij cene"

## Architektura
- [ ] Lista kolumn zduplikowana w 5 miejscach: `baza.py:15`, `baza.py:22`, `baza.py:25`, `inflacja.py:24`, `plot.py:52` + derywacja w `funkcyjki.saveCSV`
- [ ] UWAGA: `saveCSV` bierze kolejnosc z `koszyk.koszyk` - wstawienie nowej pozycji W SRODKU listy przesunie kolumny CSV wzgledem historycznych wierszy, bez ostrzezenia
- [ ] `koszyk.py` jako jedyne zrodlo definicji (nazwa, opis, URL, parser, ile kolumn), INSERT/nazwy/wykresy generowane z tego
- [ ] `requirements.txt` (requests, bs4, pandas, seaborn, matplotlib, python-dotenv)
- [ ] `.env.example` jest nietrackowany - dodac do repo, zeby bylo wiadomo jakie zmienne sa potrzebne
- [x] `python-dotenv` zastapiony wlasnym loaderem (`wczytajEnv`) - zero zaleznosci na Mikrusie, sciezka liczona od `__file__` a nie od CWD

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
- [ ] `zik.db` NADAL sledzony przez gita (sprawdzone 2026-09-03) - 588 kB snapshotu na commit. Odhaczone przedwczesnie, migracja nie zostala wykonana
- [x] `TODO` (bez rozszerzenia) - usuniete w fa8734a
- [ ] `test.py` to demo kolorow ANSI, nie test - kolory zduplikowane z `funkcyjki.py`
- [ ] `funkcyjki.znajdzSrednia` - martwy kod, jest `statistics.mean`
- [ ] Miks tabow (`skrobaczka.py`) i 4 spacji (reszta)
- [ ] `wykresuj()` zakomentowane w `zik.py:83` - wykresy w README sa z 2025-10-24
- [x] Pilnowac, zeby debugowy stan `zik.py` (`WyliczZIK()` zakomentowane, aktywne `printPage`) nie wjechal na master

## Regresje (znalezione 2026-09-03)
- [ ] PILNE: `waluty()` cofnieta do stanu z commita `4f28598` (2026-09-01 13:13). Cztery bramki awarii i `timeout=15` przestaly istniec - `git log -S` potwierdza, ze NIGDY nie byly w zadnym commicie, zyly tylko w katalogu roboczym. Do odtworzenia:
  - `timeout=15` w `requests.get`
  - zwezenie `try` do samego requestu
  - bramka `[protokol]`: `if response.status_code != 200`
  - bramka `[format]`: `try/except ValueError` wokol `json.loads` + wycinek ciala w komunikacie
  - bramka `[tresc]` a: `if not parsed.get('success')` + `parsed.get('error')`
  - bramka `[tresc]` b: lista brakujacych symboli z `('PLN','USD','XAU','CHF')`, warunek `not rates.get(s)` lapie brak, None i zero naraz
- [ ] Wniosek: poprawka bez commita nie istnieje. Commitowac natychmiast po weryfikacji, nie na koniec dnia

## Nowe znaleziska (2026-09-03)
- [ ] `saveCSV` znow wprowadzi mieszane konce linii: `open(...,'a')` bez `newline=''` + `csv.DictWriter` pisze `\r\n`, a plik jest teraz caly na `\n`. Sprawdzone. Potrzebne `newline=''` ORAZ `lineterminator='\n'`
- [ ] Tabela `zik` NIE jest rowna `ceny/xau`: 43 wiersze `kielecki` (2024-09..2025-08), 34 `chf` (2020), 1 `buty`. Dla kielecki w `zik` siedzi wartosc policzona z ceny 2.25 zl, ktora potem wyczyszczono w `ceny` do -1 (commit `22ad9f3 data clearance in db`) i zapomniano o `zik`
- [ ] `zik` powinna byc WIDOKIEM, nie tabela - jest w 100% wyliczalna z `ceny`. Migracja przetestowana na kopii: widok ma 1032 wiersze (tabela 1025, dziura znika), `plot.py` dziala bez zmian, `CASE WHEN x > 0 AND xau > 0 THEN x/xau END` zamienia `-1` i `0` na `NULL`. Likwiduje naraz: rozjazd, dziure 7 wierszy, brak atomowosci w `DBinsert`, `-1` w indeksie
- [ ] Zdublowany timestamp `2025-10-26 02:02:01` - po 2 wiersze w `ceny` i `zik`. Kazdy JOIN po timestamp mnozy wiersze (295 par przy 293 wierszach). `timestamp` nie jest dobrym kluczem
- [ ] KOLEJNOSC KOLUMN W CSV JEST ZAMROZONA. Nowe produkty tylko na KONIEC `koszyk.koszyk`, nigdy w srodku. Zademonstrowane: wstawienie `cinemacity` po `pizza` wklada cene biletu pod kolumne `maslo`, a masla pod `jablka` - bez zadnego bledu. Zapisac to w komentarzu w `koszyk.py`
- [ ] Do BeautifulSoup podawac BAJTY (`r.content`), nigdy `r.text`. `cena-pradu.pl` deklaruje `windows-1250` tylko w `<meta>`, nie w naglowku HTTP -> `requests` zgaduje ISO-8859-1 i psuje polskie znaki. `bs4` czyta meta sam i rozpoznaje poprawnie. Obecne `getPage()` robi to dobrze - nie "ulepszac"
- [ ] `prad()` zaczepiony na kodzie koloru `#0070C0`, ktory wystepuje na stronie 2x, i nadal wycina po offsetach `kod[i+8:i+30]`. Dziala (0.97), ale kazda zmiana stylowania strony to psuje. Docelowo: wyciagnac wszystkie trzy kwoty `zl/kWh` i zweryfikowac, ze dwie pierwsze sumuja sie do trzeciej z tolerancja 0.02 - wtedy parser sprawdza wlasne zrozumienie strony
- [ ] Sciezki liczone od CWD zamiast od `__file__`: `sqlite3.connect('zik.db')`, `open('zikDB.csv','a')`, `open('s.html','w')`, `plt.savefig('wykresy/...')`. Dlatego `cd` w skryptach crona jest obowiazkowy
- [ ] `if __name__ == '__main__': WyliczZIK()` + osobny `debug.py` w `.gitignore`. Dzis debugowanie wymaga edycji pliku, ktory odpala cron - stad `printPage` na origin 31.08
- [ ] `chmod 600 .env` na laptopie (jest 644) i na Mikrusie
- [ ] `.*.kate-swp` do `.gitignore` (`.zik.py.kate-swp` lezal nietrackowany)
- [ ] `runGit.sh`: zostaly 2 rzeczy - `exec >> LOG` musi byc PRZED `cd` (dzis komunikat "BLAD: brak katalogu repo" idzie na stdout, czyli pod cronem do maila), oraz `git diff --cached --quiet` przed commitem. To drugie nie jest kosmetyka: przy kolektorze chodzacym codziennie "nic do zacommitowania" ZAWSZE znaczy awarie, a dzis skrypt zameldowalby wtedy "OK: dane na origin"
- [ ] Weryfikacja crona po pierwszym piatku: `git log --format='%ad' --date=format:'%H:%M' -1` musi pokazac 03:02, nie pore lunchu

## Metoda (do stosowania przy kolejnych scraperach)
- Kazdy request ma CZTERY warstwy awarii, kazda z innym typem wyjatku i inna decyzja:
  1. TRANSPORT - siec/DNS/timeout -> `requests.RequestException`
  2. PROTOKOL - HTTP 4xx/5xx -> NIE rzuca samo, trzeba sprawdzic `status_code`
  3. FORMAT - cialo nie jest tym, czego oczekujesz -> `ValueError` / brak elementu
  4. TRESC - poprawny format, ale semantycznie blad -> `success:false`, `None` z selektora
- Warstw NIE rozdziela sie po typach wyjatkow, bo hierarchia w `requests` sie naklada: `requests.exceptions.JSONDecodeError` jest jednoczesnie `RequestException` i `ValueError`. Rozdziela sie MIEJSCEM W KODZIE - jedna bramka na warstwe, plasko
- `bigmac` psul sie na warstwie 2 (403), `upc` i `prad` na warstwie 4 - a kod raportowal identyczne "Problem z: X". Dlatego diagnoza kosztowala pol dnia
- `raise ... from None` jest konieczne, gdy oryginalny wyjatek zawiera sekret. Sanityzacja samego komunikatu NIE wystarcza - Python dokleja oryginalny traceback pod naglowkiem "During handling of the above exception". Sprawdzone: `params=` NIE chroni klucza, `requests` wkleja pelny URL do komunikatu
- Kod obslugi bledow jest jedyna czescia programu, ktora nie wykonuje sie na co dzien - dlatego zawiera bledy niewidoczne latami (`except e:` zamiast `except Exception as e:` przechodzi kompilacje i szczescliwa sciezke). Trzeba go testowac celowo, podstawiajac awarie

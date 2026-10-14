# ZIK - TODO

Przemodelowane 2026-10-12: punkty nieaktualne usuniete, rozsiane sekcje scalone tematycznie.
Legenda: `[ ]` do zrobienia, `[x]` zrobione, `[~]` swiadomie odrzucone (decyzja).

## Stan (2026-10-12)
- Martwe kolumny: 4 z 33 (na starcie pracy 13): `aspiryna`, `bigmac`, `upc`, `kasjer`
- `piwo` dziala z laptopa przez API frisco, czeka na potwierdzenie z Mikrusa
- Log: jeden format `BLAD nazwa: Typ: [warstwa] opis`, raport zdrowia (`REGRESJA`, `Martwe`) po kazdym przebiegu
- CSV jest zrodlem kanonicznym, `zik.db` to kopia zapasowa (decyzja 2026-10-06)

---

# 1. Najblizej
- [ ] AWARIA 2026-10-13/14: `e1793eb` (piwo przez API) ma w `friscoApi` 3 linie wciete SPACJAMI w pliku na tabach
      (`try`/`except` wklejone z mojego przykladu) -> `TabError` przy imporcie, zero zbierania. Stracone noce
      2026-10-13 i 2026-10-14 (ostatni wiersz 2026-10-12). Poprawka: taby, commit, push, `git pull` na Mikrusie
      przed 02:02, ewentualnie reczny `python3 zik.py` na Mikrusie, zeby uratowac 2026-10-14
- [ ] RAPORT ZDROWIA NIE ZAUWAZYL AWARII: `REGRESJA: []`, a `Martwe` liczy dni wzgledem OSTATNIEGO WIERSZA, wiec
      przy braku nowego wiersza wszystko wyglada jak wczoraj. Dodac sprawdzenie swiezosci: data ostatniego wiersza
      != dzis -> glosne `BRAK DZISIEJSZEGO WIERSZA` na samej gorze
- [ ] Przed kazdym commitem kodu: `python3 -c "import zik"` (0.2 s, bez scrapowania). Wylapalby te awarie.
      Mozna to zautomatyzowac hookiem `pre-commit` w gicie
- [x] `friscoApi`: `[protokol] HTTP {kod}` zamiast "stronka sie zepsuła", `r.json()` w try jako `[format]`
- [ ] Commit `friscoApi` + `git pull` na Mikrusie, potwierdzic piwo w logu (IP centrum danych!)
- [ ] `debug.py` (lokalnie): staly test frisco na DWOCH produktach - jednym w promocji, jednym bez.
      Test na samym produkcie w promocji nie wylapalby bledu `--highlighted` x2 z 2026-10-12
- [ ] `ruff check` na calym projekcie. Wylapuje nieuzywane parametry/importy (F841/F401) i powtorzone klucze
      slownika (F601) - 3 bledy z lekcji A. `from skrobaczka import *` utrudnia mu prace (F403/F405)
- [ ] Obserwowac w logu: czy piwo/frisco dostaja w nocy 503/429 (od 2026-10-12 log to rozroznia od `[tresc]`)

# 2. Martwe zrodla
- [ ] `aspiryna` (wapteka.pl) i `bigmac` (ubereats) - HTTP 403 z IP Mikrusa, z laptopa dzialaja, parsery dobre.
      Hipoteza: blokada zakresow centrow danych. Do sprobowania: naglowki jak przy JSON (`Accept`,
      bez `Sec-Fetch-Dest: document`), albo API sklepu jak przy fryzjerze/piwie, albo inne zrodlo.
      bigmac: ciaglosc 11.30 (2020) -> 22.90 (2024) -> 24.70 (2026-08 recznie)
- [ ] `upc` - 900 kB HTML, cena renderowana JS-em. Szukac API, z ktorego bierze ja strona
- [ ] `kasjer` (jobted.pl) - 984 B HTML, sciana zgody/antybot. Prawdopodobnie inne zrodlo
- [ ] Metoda, ktora zadzialala 2x (fryzjer, piwo): zamiast parsowac HTML, sprawdzic w bundlu JS strony,
      skad jej aplikacja bierze dane - zwykle jest publiczne API pod inna sciezka

# 3. Frisco -> API
- [ ] Po tygodniu stabilnego piwa przeniesc wszystkie 9 produktow frisco z HTML (`--highlighted/--emphasized`) na
      `friscoApi`. Sprawdzone 2026-10-12: maslo 5.89, jajka 13.99 - zgodne z HTML
- [ ] PRZED przenosinami: ktore pole odpowiada `--highlighted`? `price` (w gazetce juz promocyjna,
      regularna w `priceBeforeDiscount`) vs `priceAfterPromotion` (promocja warunkowa, np. marchew 2.49 -> 1.39).
      Decyzja z 2026-09-29: zapisujemy cene promocyjna, jesli jest
- [ ] Po przenosinach: ponowienie frisco w `skanujKoszyk` prawdopodobnie zbedne

# 4. Jakosc danych
- [ ] Walidacja skokow: zmiana >30% wzgledem ostatniej dodatniej wartosci = flaga w raporcie zdrowia.
      Raport lapie `-1`, ale NIE lapie cichych smieci (prad 0.0, jablka 0.0, telefon 179 zl za etui, buty 239 -> 549)
- [ ] `buty` skoczyly 239 -> 259 -> 549 (2026-09-06..08) i stoja na 549. `getPageClass(url,'price')` bierze
      PIERWSZA cene na liscie, niekoniecznie najtansza. Sprawdzic
- [ ] `otomoto`: `if len(kwota) < 100: raise` - przy zepsutej paginacji mediana spadnie o polowe bez bledu
- [ ] `prad()` zaczepiony na kolorze `#0070C0` i offsetach `kod[i+8:i+30]`. Docelowo: wyciagnac trzy kwoty
      `zl/kWh` i sprawdzic, ze dwie pierwsze sumuja sie do trzeciej (tolerancja 0.02)
- [ ] Opisy w `koszyk.py` rozjechane z URL-em: `mydlo` (Bialy Jelen 150g vs "barwa mydlo szare"),
      `kindle` (8gb vs URL 16gb). Telefon juz poprawiony
- [ ] Historia `telefon` niewiarygodna: 62 skoki >10% na 888 odczytow (akcesoria 119-542 zl, ceny x100 typu
      638900, oscylacje 3598 <-> 7998). Bez stalego przelicznika - uznac kolumne za uzyteczna od 2026-09-09
      albo recznie oczyscic
- [ ] `lot`: 12 odczytow do 2020-05-06 to cena jednego dnia, od 2026-09-09 mediana miesiaca. Stare oznaczyc `-1`
- [ ] `szukajJsonLD` porownuje `@type` doslownie - nie znajdzie `'http://schema.org/Product'`. Przy kolejnym
      sklepie porownywac koncowke
- [ ] `telefon`: przy najblizszej promocji sprawdzic, czy JSON-LD deluxury podaje cene promocyjna czy regularna
- [ ] `m2`: strona podaje filtr wprost (`od 50 m² do 60 m²`) - walidacja filtra jednym regexem (opcjonalnie)

## Tabela zmian produktu
Metadana potrzebna analityce (pionowa kreska na wykresie zamiast falszywej inflacji).
- [ ] Wprowadzic tabele/plik `(produkt, data_od, opis, url)`. Znane zmiany:
  - `telefon`: S25 Ultra 256GB (do 2026-09-06, 3648) -> S26 Ultra 256GB (od 2026-09-09, 4253). +16.6% to NIE inflacja
  - `piwo`: pid 3192 (wycofany, `substituted-by 153955`) -> pid 153955, ten sam czteropak. Przerwa 2026-01 .. 2026-10
  - `aspiryna`: URL `/aspirin-500-mg-10-tabletek-2621,p` -> `/produkt/aspirin-10-tabl,3795/` (ten sam produkt)
  - `lot`: cena dnia -> mediana miesiaca KRK-CIA (2026-09-09)
  - `fryzjer`: API rezerwacje-jeanlouisdavid.pl -> jld.pl (ten sam salon M58 i usluga, 2026-10-08)
  - `frisco` x9: zrodlo HTML -> API (jesli dojdzie do skutku)

# 5. Dane: CSV i baza
- [ ] `-1` jako sentinel zatruwa obliczenia: docelowo `NULL` / pusta komorka. Tabela `zik` zapisuje `-1/xau` jak legalna wartosc
- [ ] Zejscie z bazy: `plot.py`, `inflacja.py` i modul analityki czytaja z bazy - przepiac na CSV
- [ ] Do czasu zejscia, znane wady bazy:
  - rozjazd: 3 wiersze z 2020 tylko w CSV, 7 z 2021 tylko w bazie
  - `zik` != `ceny/xau` w 43 wierszach `kielecki`, 34 `chf`, 1 `buty` (stare czyszczenie `ceny` bez `zik`)
  - `zik` powinna byc WIDOKIEM (`CASE WHEN x > 0 AND xau > 0 THEN x/xau END`) - przetestowane na kopii
  - zdublowany timestamp `2025-10-26 02:02:01` - JOIN po timestamp mnozy wiersze
  - `DBinsert` - dwa osobne commity zamiast jednej transakcji, polaczenia sqlite nigdy nie zamykane
- [ ] Dziura 2026-09-11..17 (7 dni) - nie do odtworzenia, nie ma jej nigdzie
- [ ] KOLEJNOSC KOLUMN W CSV JEST ZAMROZONA - nowe produkty tylko na KONIEC `koszyk.koszyk`. Wstawienie w srodek
      przesuwa kolumny bez bledu. Zapisac to komentarzem w `koszyk.py`

# 6. Architektura i porzadki w kodzie
- [ ] Lista kolumn w 5 kopiach: `baza.py` (3x), `inflacja.py:24`, `plot.py:52`. `koszyk.py` powinien byc jedynym
      zrodlem (nazwa, opis, URL, scraper, ile kolumn) - wtedy znika tez slownik SCRAPERY w `zik.py`
- [ ] Sciezki liczone od CWD: `sqlite3.connect('zik.db')`, `open('zikDB.csv')`, `open('s.html')`,
      `plt.savefig('wykresy/...')`. Liczyc od `__file__`, jak `ENV` w `skrobaczka.py`
- [ ] `requirements.txt` + wlasny venv projektu. Na laptopie shell siedzi w venvie CRM (bez bs4), systemowy
      `/usr/bin/python3.14` nie ma matplotlib/seaborn - `plot.py` nie ruszy nigdzie
- [ ] `.env.example` do repo (jakie zmienne sa potrzebne)
- [ ] Martwy kod: `kindle.py`, `test.py` (demo kolorow ANSI), `funkcyjki.znajdzSrednia`, `koszyk.getProduct`
- [ ] Miks tabow (`skrobaczka.py`) i 4 spacji (reszta) - 2026-10-13 kosztowal 2 noce danych (`TabError`)
- [ ] `wykresuj()` zakomentowane - wykresy w README sa z 2025-10-24 (nalezy do modulu analityki)
- [~] `sprawdz_waluty.py` do repo - DECYZJA 2026-09-03: nie. Nic nie pilnuje czterech bramek w `waluty()`

# 7. Operacje: Mikrus, cron, git
- [ ] `runGit.sh` i `runZik.sh` nie sa w repo (leza w `/home/frog/zik/`) - bez historii i kopii. Rozwazyc `bin/`
- [ ] Do sprawdzenia w obu skryptach: `exec >> LOG` PRZED `cd` (inaczej "BLAD: brak katalogu repo" idzie
      pod cronem do maila), w `runGit.sh` `git diff --cached --quiet` przed commitem (przy codziennym
      kolektorze "nic do commita" = awaria)
- [ ] `webmaker.sh:27` debugowy `echo "zajecia $zajecia"` dubluje log od 2024-08-07 (1269 razy).
      Usunac, potem rozwazyc oczyszczenie `zikFull.log` z duplikatow
- [ ] `chmod 600 .env` na Mikrusie (laptop juz ma 600)
- [ ] `.gitignore`: usunac `# Projektowe` / `#zik.db` (linie 2-3, regula jest w 135), dodac `.*.kate-swp`
- [ ] Historia gita: 53.74 MiB (stare bloby `zik.db`, `s.html` 30 MB, `lazygit` 21 MB). Odchudzenie =
      `git filter-repo` + force-push + swiezy klon na Mikrusie. Do rozwazenia, czy warto
- Zasady: Mikrus commituje DANE, laptop KOD. Nie edytowac sledzonych plikow na Mikrusie (blokuje `pull --rebase`).
  Kod na Mikrusie zmienia sie tylko w piatek 03:02 albo po recznym `git pull`

# 8. Waluty
- [ ] fixer.io podaje XAU z 6 miejscami (`0.00026`) - krok kwantyzacji ~0.4% ceny zlota, caly indeks skacze co 0.4%
- [ ] Zbierac rownolegle zloto z NBP (`api.nbp.pl/api/cenyzlota`, 1 g, bez klucza, historia od 2013) w nowej
      kolumnie NA KONCU CSV

# 9. Modul analityki (zaprojektowany 2026-09-10)

Zasada: **pomiar jest nieodtwarzalny, wyliczenie jest odtwarzalne**. Nic odtwarzalnego nie ma prawa stac
miedzy kolektorem a zapisem pomiaru. `calculateInflation()` wyjete z kolektora 2026-09-10.

Co nalezy do modulu:
- [ ] Inflacja Y2Y per pozycja + agregaty FOOD / Commodities / Luxury
- [ ] Indeks ZIK (cena/xau) - wyliczany, nie zapisywany
- [ ] Wykresy (`plot.py`)
- [ ] Wykorzystanie tabeli zmian produktu (sekcja 4)

Bledy `inflacja.py` do naprawienia przy przenoszeniu:
- [ ] `nowe < 0` nieobslugiwane (tylko `stare < 0`) - pozycja z `-1` wchodzi jako -100%. 2026-09-10: FOOD 274.8%
- [ ] `DBgetNotNullValue` bierze ostatnia dodatnia wartosc z DOWOLNEJ daty - "Y2Y" nie jest Y2Y
- [ ] `try` obejmuje cala petle - jeden wyjatek zostawia zera w `statistics.mean`. Try per pozycja
- [ ] Twarde indeksy w `luxuryInflation`/`commoditiesInflation` (`inf[11:13]`, `inf[31]`...) - adresowac po nazwie
- [ ] Kategorie jako DANE (slownik nazwa -> kategoria), nie komentarz. Dzis komentarz i kod sie nie zgadzaja

Decyzje do podjecia:
- [ ] Pozycja bez danych: pominac w sredniej (uczciwe, ale zmienia liczbe skladnikow) czy inaczej?
- [ ] Wagi: dzis Rolex i majonez wazą tyle samo
- [ ] Podmiany produktu: pominac dzien podmiany czy przeliczac na styk?
- [ ] Wyjscie: print, plik czy strona przez `webmaker.sh`?
- [ ] Punkt wejscia: `analiza.py` na zadanie, tylko do odczytu, osobno od crona zbierajacego

# 10. Pomysly
- [ ] Koszyk: cinemacity, wiecej sklepow, srednia z kilku jajek/kurczakow, najtansze jablka
- [ ] Side projekt: kiedy najlepiej kupic lot (zaczac od 6 miesiecy przed)
- [ ] Strona internetowa

---

# WIEDZA (nie zadania)

## Metoda: cztery warstwy awarii
1. TRANSPORT - siec/DNS/timeout -> `requests.RequestException`, zawsze `timeout=`
2. PROTOKOL - HTTP 4xx/5xx -> samo nie rzuca, sprawdzic `status_code`
3. FORMAT - cialo nie jest tym, czego oczekujesz -> `ValueError` z `json`, brak elementu
4. TRESC - poprawny format, zly sens -> `success:false`, `None`, zero, brak produktu
- Warstwy rozdziela MIEJSCE w kodzie, nie typ wyjatku (`requests.exceptions.JSONDecodeError` jest i `RequestException`, i `ValueError`)
- `raise ... from None`, gdy oryginalny wyjatek zawiera sekret - `params=` NIE chroni klucza
- Kod obslugi bledow nie wykonuje sie na co dzien, wiec trzeba go testowac celowo (np. `print(f'... {x[0]}')` w galezi ponowienia)

## Zasady wyniesione z pracy
- Awarie oczekiwane -> `-1` (w `pobierz`). Bugi -> maja byc widoczne (`TypeError`, `NameError` w logu = kod, nie strona)
- Zero to nie cena, to porazka parsera (`prad 0.0`, `jablka 0.0`) - `raise`, nie zapis
- Wybierac dane po ZNACZENIU, nie po pozycji (`oferty[1]`, `products[0]`, offsety w tekscie, `x[0]`)
- Prawie identyczne linie ukrywaja roznice jednego slowa (`upc -> prad`, `--highlighted` x2, klucze x3 w slowniku)
- Ponawianie tego samego URL zamienia awarie przelotna w trwala (piwo 0/44). JEDNA proba z przerwa to sufit
- Testy potrafia same wywolac wynik, ktory mierza (40 prob piwa, dwa rownolegle skany -> 503)
- Refaktoryzacja zmienia strukture, nie wynik - porownac wartosci przed i po (`prettify()` w `getPage` musi zostac)
- Przy zmianie sygnatury grep po WSZYSTKICH wywolaniach (`zrobCene` w `lekarz`)
- Poprawka bez commita nie istnieje. Debug nie trafia na produkcje (`debug.py` w `.gitignore`, `__main__`)
- Do BeautifulSoup podawac bajty (`r.content`) - cena-pradu.pl deklaruje `windows-1250` tylko w `<meta>`
- `.get_text()` na `<script>`, nie `.string` (`.string` daje `None` -> `TypeError`, ktorego `except ValueError` nie zlapie)
- Datacenter IP dostaje gorsze traktowanie (wapteka/ubereats 403) - testy z laptopa tego nie pokaza

## Archeologia danych frisco (ustalona 2026-09-04, przeliczona 2026-10-09)
- do 2025-05-23 cena PRODUKTU | 2025-05-24..2025-12-11 cena JEDNOSTKOWA | 2025-12-12..2026-03-03 PRODUKTU |
  2026-03-04..2026-09-04 JEDNOSTKOWA | od 2026-09-05 PRODUKTU (selektor `f-pdp__`)
- Przeliczone skryptem `przelicz_frisco.py` (commit `22c5123`): 2868 komorek, przeliczniki kielecki 0.7, pizza 0.425,
  maslo 0.2, makaron 0.4, chleb 0.5, mydlo 0.1, kurczak 0.5, piwo 2.0. Szwy zgadzaja sie co do grosza
- `chleb` w oknie 1 (0.09..0.98) -> `-1`: losowy element strony, nie cena jednostkowa
- [~] `kielecki` 2021-11-25 i 2025-05-08 - przelicznik 1.43 nie do odroznienia od zmiany ceny, nie ruszamy
- [~] Mieszanie ceny promocyjnej i regularnej w historii - nie do odtworzenia
- Klasy CSS koduja STAN ceny: `--emphasized` bez promocji, `--highlighted` promocja, `--plain` przekreslona regularna
- Piwo: bramka wieku (`popup/are-you-adult`), nie IP ani wariant frontendu. API wyszukiwarki jej nie ma

## Zrodla, ktore dzialaja (dla przyszlych napraw)
- frisco API: `https://www.frisco.pl/app/commerce/api/v1/offer/products/query?search=...`, wybor po `product.id`
- JLD: `https://jld.pl/api/salon-prices/M58` + naglowki `X-API-Version: 4`, `X-Brand: JLD`, `X-Client-Name: web`
- Ryanair: `services-api.ryanair.com/farfnd/v4/oneWayFares/KRK/CIA/cheapestPerDay`, bez klucza
- otomoto: JSON-LD, `priceSpecification.price`, petla `&page=N` do pustej strony - TYLKO pelne przejscie trzyma ciaglosc
- deluxury: JSON-LD `Offer` z filtrem `@id` konczacym sie na id produktu (inaczej akcesoria)
- Morizon: kotwica tekstowa `Średnia cena:.*?\(\s*([\d\s\xa0]+)\s*zł/m`

---

# ARCHIWUM ZROBIONYCH (skrot)
- [x] 2026-09-03 `zik.db` odsledzony, `lazygit` do `.gitignore`, `user.name=mikrus`, `prad` naprawiony (0.97), stare 500 wierszy `0.0` -> `-1`
- [x] 2026-09-03 `waluty()` odtworzona: https, `timeout`, klucz w `.env`, `from None`, cztery bramki. Wlasny loader `.env`
- [x] 2026-09-04 cron `homr` -> `home`, Mikrus odblokowany (niezacommitowany `.gitignore`)
- [x] 2026-09-05 `frisco()` na `f-pdp__` (9 produktow), `jajka` wrocily po 185 dniach
- [x] 2026-09-09 `lot` po 988 dniach (mediana miesiaca), `telefon` -> S26, `getJsonLD` + `szukajJsonLD`
- [x] 2026-09-10 `saveCSV` z `newline=''` i `lineterminator='\n'`, ponowienie frisco, inflacja wyjeta z kolektora
- [x] 2026-09-29/30 frisco `--highlighted`/`--emphasized` + `cena == 0` raise, `raport.py` (REGRESJA, Martwe posortowane)
- [x] 2026-10-06 `__main__` + `debug.py`, `DBinsert` przywrocony + baza uzupelniona z CSV, `m2` kotwica tekstowa
- [x] 2026-10-07/08 `telefon` JSON-LD, `auto` x2 po 744 dniach (pelna paginacja), `fryzjer` nowe API, cookies z 2021 wyciete
- [x] 2026-10-09 historia frisco przeliczona (2868 komorek), `^M` w CSV usuniete
- [x] 2026-10-09/12 lekcja A: `pobierz`, jeden format bledow, `zrobCene` rzuca, slowniki SCRAPERY/PODWOJNE/WALUTY
- [x] 2026-10-12 lekcja B: `pobierzSoup` (transport/protokol dla wszystkich), frisco jednym requestem, martwe helpery usuniete
- [x] 2026-10-12 piwo: przyczyna (bramka wieku) + `friscoApi`, nowy pid 153955, 17.59 z laptopa
- Klasa awarii "debug na produkcji" wystapila 5 razy (printPage, `# WyliczZIK()` -> 7 dni, edycja na Mikrusie ->
  backup 3 tyg., `# DBinsert` -> tydzien bazy). Zamknieta przez `__main__` + `debug.py`

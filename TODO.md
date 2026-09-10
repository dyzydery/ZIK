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
- [x] `timeout=15` dodany do WSZYSTKICH funkcji pomocniczych 2026-09-04 (`getPage`, `getPageHeader`, `printPage*`, `getPageClass*`, `getPageId`, `getJsonLD`). Cron nie moze juz zawisnac bez konca, a istniejace `except requests.RequestException` przestaly byc martwym kodem
- [ ] `getPageClass(url, klasa, timeout=15)` - parametr `timeout` jest ZADEKLAROWANY, ale w srodku jest na sztywno `timeout=15`. Parametr jest ignorowany, czyli sygnatura klamie. Uzyc go albo usunac
- [x] `waluty()` - klucz w `.env`, `from None`, `timeout=15`, `https`, cztery bramki awarii (transport/protokol/format/tresc). Zweryfikowane sprawdzarka 6/6
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
- [ ] `piwo` - NIE jednolinijkowiec. URL rzeczywiscie redirectuje na `pid,153955` (2 l, ten sam produkt), ale `frisco()` czyta wtedy 8.79 = cene ZA LITR. Prawdziwa cena czteropaku to 17,59. Naprawa razem z `frisco()` nizej
- [x] `aspiryna` NAPRAWIONA 2026-09-04: nowy URL `https://www.wapteka.pl/produkt/aspirin-10-tabl,3795/` w `koszyk.py` + parser na JSON-LD zamiast klas CSS. Zwraca 9.47. UWAGA: poprawka literowki (`produkt = e` -> `produkt = encja`) byla tylko ZASTAGOWANA, commit `10f3d8a` na origin ma jeszcze zepsuta wersje - do zacommitowania
- [ ] `fryzjer` - API `/api/salon-prices/M58` nie istnieje, redirect na strone glowna
- [ ] `jajka` - NIE jest martwe! Produkt jest dostepny, cena 13,99. Stary parser czytal `price_num`, ktorego na tej stronie nie ma. Naprawia sie samo po zmianie selektora `frisco()`
- [ ] `lot` - SPA, cena tylko z JS (3.5 kB HTML), trzeba API Ryanaira
- [ ] `auto`, `m2wtorny`, `m2pierwotny` - strona wraca 200 z pelna trescia, tylko selektory nie pasuja
- [ ] `upc` - NIE selektor: 493 kB HTML ale tylko 1577 znakow tekstu, tresc renderowana JS-em
- [ ] `kasjer` - NIE selektor: 987 B HTML, 74 znaki tekstu, sciana bot/consent
- [ ] `auto` i `m2` opieraja sie na hashowanych klasach CSS (`efpuxbr16 ooa-1n2paoq er34gjf0`, `data-v-0d6d0a35`) - to sie zmienia przy kazdym deployu strony. Przepisac na JSON-LD / `__NEXT_DATA__` / `data-testid`
- [ ] `aspiryna()` i `frisco()` robia 2x request na ta sama strone - rozdzielic "pobierz strone" od "wyciagnij cene"

## frisco() czyta cene jednostkowa zamiast ceny produktu (2026-09-04)
- [ ] KRYTYCZNE: klasa `price_num` na frisco.pl to CENA ZA KG/LITR, nie cena produktu. Dotyczy 9 z 33 kolumn - calego rdzenia koszyka spozywczego. Arytmetyka zgadza sie co do grosza: kielecki 14,19/0,7 l = 20,27 | pizza 10,29/0,425 kg = 24,21 | maslo 5,89/0,2 = 29,45 | makaron 5,19/0,4 = 12,97 | chleb 4,69/0,5 = 9,38 | piwo 17,59/2 l = 8,79
- [ ] Wlasciwy selektor: `f-pdp__price-amount--emphasized` (pdp = product detail page, konwencja BEM, nie hash z bundlera). Sprawdzony na 10 produktach, dziala na wszystkich - w tym na `jajka`, gdzie `price_num` w ogole nie istnieje
- [ ] Zmiana selektora naprawia naraz: kielecki, pizza, maslo, jablka, makaron, chleb, mydlo, kurczak, jajka, piwo
- [ ] Przywraca tez ZNACZENIE historyczne: pierwszy odczyt kielecki z 2020 to 8,99 czyli cena produktu, nie 12,8 zl/l. Nowy selektor wraca do tego, co mierzono na poczatku
- [ ] Przy okazji naprawic bug `zakg`: `if (url.find('chleb')):` jest zawsze prawdziwe, wiec indeks to zawsze 1. Po przejsciu na `f-pdp__` caly `zakg` znika, bo jest dokladnie jeden element z cena produktu
- [ ] Dane historyczne z frisco sa niewiarygodne, nie tylko przesuniete: `chleb` skacze 17.99 (2024-09) -> 13.99 (2024-12) -> 0.09 -> 0.95 -> 0.19 -> 0.96 (maj 2025). To parser lapiacy losowy element zaleznie od liczby promocji na stronie. Do decyzji, co z tym zrobic - podobnie jak z `prad`
- [ ] Opis `mydlo` w koszyku mowi 150 g, a `f-pdp__` daje 4,59 - sprawdzic gramature, bo stare 45,90 to bylo zl/kg


## Co sie stalo w danych frisco - archeologia (ustalone 2026-09-04)

Metoda: szukanie skokow, ktorych stosunek odpowiada przelicznikowi cena_jednostkowa/cena_produktu
(czyli 1/gramatura). Daty zgadzaja sie dla WSZYSTKICH produktow naraz, wiec to zmiany po stronie
frisco.pl, nie przypadek.

- **do 2025-05-23** - cena PRODUKTU, w wiekszosci poprawna
- **2025-05-24 .. 2025-12-11** - przelaczenie na cene JEDNOSTKOWA (zl/kg, zl/l).
  Skoki tego dnia: pizza x2.35, maslo x5.00, makaron x2.35, mydlo x10.00
- **2025-12-12 .. 2026-03-03** - powrot do ceny PRODUKTU.
  Skoki: pizza /0.425, maslo /0.20, makaron /0.40, mydlo /0.10, kurczak /0.50, piwo /2.00
- **2026-03-04 .. dzis** - znowu cena JEDNOSTKOWA.
  Skoki: kielecki x1.428, pizza x2.353, maslo x5.00, makaron x2.499, chleb x2.00, mydlo x10.00, kurczak x2.00

Czyli w ostatnich 16 miesiacach okolo 12,5 miesiaca danych to cena za kg/litr zamiast ceny produktu.
Przelicznik jest znany i staly, wiec te okresy DA SIE przeliczyc wstecz - w odroznieniu od `prad`,
gdzie trzeba bylo skasowac.

- [ ] Zdecydowac, co z okresami jednostkowymi: przeliczyc przez gramature (przelicznik znany co do grosza)
      czy oznaczyc jako `-1`. Przeliczenie jest tu obronialne, bo to ta sama wielkosc w innej jednostce,
      a nie inny produkt
- [ ] `kielecki` ma najmniejszy przelicznik (1.428), wiec jego skoki z 2021-11-25 i 2025-05-08 moga byc
      zwyklymi zmianami ceny, nie przelaczeniem. Pewne jest tylko 2026-03-04
- [ ] `chleb` to osobna awaria, nie przelaczenie jednostki: od 2025-06 wartosci 0.09 / 0.19 / 0.47 / 0.53 /
      0.95 / 0.99 oscylujace z dnia na dzien. Parser lapal cos zupelnie innego (ocena? cena za 100 g?).
      Zbadac osobno przed decyzja o przeliczeniu

## piwo - dlaczego nadal `-1` po naprawie frisco() (2026-09-04)
- [ ] frisco.pl serwuje DWA warianty strony produktu, niedeterministycznie, dla tego samego URL:
      wariant nowy ~1,58 MB z klasa `f-pdp__price-amount--emphasized` (cena 17,59)
      wariant stary ~518 kB, bez zadnej klasy `f-pdp__*`, w tekscie zero kwot `X,XX zl`
- [ ] Rozklad jest ZALEZNY OD PRODUKTU, zmierzony na 8 probach: kielecki 8/8 nowy, chleb 8/8 nowy,
      piwo tylko 3/8 nowy. Dlatego `piwo` wraca `-1`, a reszta dziala
- [ ] To NIE jest kwestia przekierowania - sprawdzone, ten sam URL bez redirectu tez czasem daje stary wariant
- [ ] To NIE jest weryfikacja wieku - w wariancie bez ceny nie ma zadnych markerow typu "pelnoletni",
      "18 lat", "weryfikacja"
- [ ] Mozliwe podejscia do rozwazenia: powtorzenie requestu az do trafienia w nowy wariant (z limitem prob),
      albo parser obslugujacy oba uklady - ale w starym wariancie jest wylacznie cena jednostkowa,
      wiec ceny produktu nie da sie stamtad odczytac wcale
- [ ] URL piwa w `koszyk.py` to nadal stary `pid,3192` (redirectuje na `pid,153955`) - do aktualizacji
      niezaleznie od powyzszego

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
- [x] `zik.db` ODSLEDZONY 2026-09-03 w `9d1412c`. Zrobione na Mikrusie (autor commita: `mikrus`), wiec serwer zachowal plik na dysku, a laptop stracil swoja kopie przy pullu - tak mialo byc. `runGit.sh` wysyla juz tylko `zikDB.csv`. Baze do `plot.py` sciagac `scp`-em poza gitem
- [x] Odroznic maszyny w historii gita - `user.name=mikrus` ustawione na serwerze, widac w autorze commitow
- [ ] Historia gita nadal wazy 53.74 MiB i trzyma ~16.6 MB starych blobow `zik.db` + 30.9 MB `s.html` + 20.8 MB `lazygit`. Odsledzenie zatrzymuje TYLKO dalszy wzrost. Odchudzenie wymaga `git filter-repo` i force-pusha, plus swiezego klona na Mikrusie - do rozwazenia, czy warto
- [x] `TODO` (bez rozszerzenia) - usuniete w fa8734a
- [ ] `test.py` to demo kolorow ANSI, nie test - kolory zduplikowane z `funkcyjki.py`
- [ ] `funkcyjki.znajdzSrednia` - martwy kod, jest `statistics.mean`
- [ ] Miks tabow (`skrobaczka.py`) i 4 spacji (reszta)
- [ ] `wykresuj()` zakomentowane w `zik.py:83` - wykresy w README sa z 2025-10-24
- [x] Pilnowac, zeby debugowy stan `zik.py` (`WyliczZIK()` zakomentowane, aktywne `printPage`) nie wjechal na master

## Regresje (znalezione 2026-09-03)
- [x] `waluty()` ODTWORZONA i zacommitowana w `039a113` (2026-09-03). Sprawdzone: 6/6 przypadkow przechodzi, `timeout=15` obecny, `https` zamiast `http`. Cztery bramki awarii:
  - `timeout=15` w `requests.get`
  - zwezenie `try` do samego requestu
  - bramka `[protokol]`: `if response.status_code != 200`
  - bramka `[format]`: `try/except ValueError` wokol `json.loads` + wycinek ciala w komunikacie
  - bramka `[tresc]` a: `if not parsed.get('success')` + `parsed.get('error')`
  - bramka `[tresc]` b: lista brakujacych symboli z `('PLN','USD','XAU','CHF')`, warunek `not rates.get(s)` lapie brak, None i zero naraz
- [x] Wniosek: poprawka bez commita nie istnieje. Commitowac natychmiast po weryfikacji, nie na koniec dnia
- [~] `sprawdz_waluty.py` - DECYZJA 2026-09-03: nie dorzucamy do repo. Konsekwencja: nic nie pilnuje czterech bramek w `waluty()`, wiec kolejna regresja przejdzie niezauwazona az do awarii fixera. Jesli kiedys wroci - test lezal w scratchpadzie sesji

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
- [x] CRON DZIALA - poprawka `homr`->`home` zadzialala. Log ma wpis `Fri Sep  4 03:02:00 CEST 2026`, czyli skrypt ruszyl punktualnie. Brak commita na origin wynikal z czego innego (nizej)
- [x] MIKRUS ODBLOKOWANY 2026-09-04 - commity `37c0be6` (dane z piatku) i `0dbf05c` (`.gitignore`) sa na origin, rebase przeszedl czysto. Przyczyna byla: niezacommitowana zmiana w `.gitignore`, ktora jest brakujaca druga polowa migracji. Commit `9d1412c` z Mikrusa zawieral tylko `git rm --cached zik.db`, a dopisanie `zik.db` do `.gitignore` nigdy nie zostalo zacommitowane. Origin ma w linii 3 `#zik.db` (zakomentowane, zgodnie z krokiem 1 planu). Odblokowanie: `git add .gitignore && git commit && git push` - rebase NIE jest potrzebny, bo `a833e78` siedzi wprost na `origin/master`
- [ ] Piatkowe dane sa bezpieczne: sprawdzone, `git add zik.db zikDB.csv` na ignorowanej sciezce zwraca kod 1, ALE mimo to stawia `zikDB.csv` w indeksie. Blad w logu to halas, nie awaria zapisu
- [ ] Po commicie `.gitignore` bedzie mial dwa wpisy o tym samym: `#zik.db` w linii 3 (komentarz) i `zik.db` na koncu (regula). Usunac `#zik.db` i `# Projektowe`, zeby plik nie klamal
- [ ] Przebieg z logu, dla historii:
  1. `git add zik.db zikDB.csv` -> `The following paths are ignored by one of your .gitignore files: zik.db`. Dokladnie mina nr 2 z planu migracji - `runGit.sh` nadal dodaje odsledzony plik
  2. `git commit` mimo to przeszedl -> lokalny commit `a833e78` (1 plik, `zikDB.csv`)
  3. `git pull --rebase` -> `error: cannot pull with rebase: You have unstaged changes`
  4. `git rebase --abort` -> `fatal: No rebase in progress?` - dokladnie ten szum, ktory zapowiadalem przy awarii innej niz konflikt
  5. `exit 1`, pusha nie bylo. Commit `a833e78` siedzi lokalnie i nie wychodzi na origin
- [ ] Wczesniejszy przebieg (2026-09-03 14:14) pokazuje, czemu binarna baza w gicie byla zla: `Cannot merge binary files: zik.db` + `CONFLICT (content): Merge conflict in zik.db` ORAZ w `zikDB.csv`. Odsledzenie `zik.db` usunelo polowe problemu, druga polowa (CSV) zostaje
- [ ] `runGit.sh` i `runZik.sh` NIE SA W REPO - leza w `/home/frog/zik/`, obok katalogu projektu. Dlatego commity "runGit: tylko CSV" (`5e518b9`, `7205cc4`) zmienily `TODO.md` i `.gitignore`, ale samego skryptu nie tknely. Poprawke trzeba wprowadzic recznie na Mikrusie
- [ ] Rozwazyc wciagniecie obu skryptow do repo (np. katalog `bin/`) - dzis nie ma ich historii, nie ma kopii, i nie da sie ich zmienic przez gita

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

## Zrobione 2026-09-04
- [x] `frisco()` - selektor `f-pdp__price-amount--emphasized` zamiast `price_num`. Naprawia 9 produktow naraz. Zweryfikowane: kielecki 14,19 | pizza 10,29 | maslo 5,89 | jablka 6,19 | makaron 5,19 | chleb 4,69 | mydlo 4,59 | kurczak 24,19 | jajka 13,99. Bug `zakg` znikl razem ze starym selektorem
- [x] `prad` potwierdzony NA PRODUKCJI - piatkowy run 2026-09-04 02:02 zapisal 0.97 (czwartek: -1)
- [x] `getJsonLD(url)` - nowa funkcja pomocnicza. Obsluguje wszystkie trzy legalne ksztalty JSON-LD (jeden obiekt / lista / `@graph`), splaszcza do jednej listy encji przez `extend`, pomija zepsute bloki przez `continue` zamiast unieważniać wszystkie. Do wykorzystania przez `bigmac`, `m2`, `auto`
- [x] `testowyZIK()` - osobna funkcja do debugowania w `zik.py`, zamiast edytowania linii wykonywanych przy imporcie. Pol kroku do `if __name__ == '__main__'`

## Nowe znaleziska 2026-09-04
- [ ] `except Exception as e` TWORZY zmienna lokalna calej funkcji. Uzycie `e` w ciele `try`, przed handlerem, daje `UnboundLocalError: cannot access local variable 'e'` - ktory ten sam handler lapie i zamienia na ciche `-1`. Tak wlasnie `aspiryna()` zwracala -1 mimo poprawnej logiki. Gdyby handler byl wezszy (`except (ValueError, AttributeError, KeyError)`), bug przelecialby na wierzch i krzyknal. Praktyczny argument za regula: awarie oczekiwane -> `-1`, bugi -> krzyk
- [ ] Zdegenerowane odpowiedzi w `aspiryna()` daja `-1`, ale komunikaty sa nierozroznialne: brak encji Product, zero encji i brak `offers` wszystkie dawaly `'NoneType' object has no attribute 'get'`. Czesciowo naprawione jawna bramka `if produkt is None`. Ten sam problem maja pozostale scrapery
- [ ] `getProduct(url)` zwraca `None`, gdy URL nie jest DOKLADNIE tym z `koszyk.py` - widac w komunikatach "Problem z: None". Handler, ktory nie umie podac nazwy produktu, jest o tyle mniej uzyteczny
- [ ] Do BeautifulSoup podawac `.get_text()` na tagu `<script>`, nie `.string`. `.string` zwraca `None`, gdy tag ma wiecej niz jedno dziecko albo jest pusty - i wtedy `json.loads(None)` rzuca `TypeError`, ktorego `except ValueError` NIE zlapie. `.get_text()` na pustym tagu daje `''`, czyli `JSONDecodeError`, czyli `ValueError`. Jeden typ wyjatku zamiast dwoch
- [ ] Kolejnosc warunkow przy rozpoznawaniu ksztaltu JSON-LD: `isinstance(dane, list)` MUSI byc przed `'@graph' in dane`, bo `in` na liscie szuka elementu, nie klucza - lista `['@graph']` dalaby prawde

## Do sprawdzenia w sobote 2026-09-05
- [ ] Sobotni run o 02:02 to pierwszy z naprawionym `frisco()`. Oczekiwane wartosci: kielecki 14,19 (dzis 20,27) | chleb 4,69 (dzis 9,38) | jajka 13,99 (dzis -1) | maslo 5,89 | makaron 5,19. Jesli kielecki nadal pokaze 20,27 - Mikrus nie ma kodu
- [ ] `piwo` moze nadal dac `-1` - szansa na dobry wariant strony to 3/8
- [ ] `aspiryna` da 9.47 TYLKO jesli zacommitujesz poprawke literowki przed 02:02

## Zrobione 2026-09-08/09 - potwierdzone w produkcji
- [x] `frisco()` DZIALA od 2026-09-05: kielecki 14.19, pizza 10.29, maslo 5.89, jablka 6.49, makaron 5.19, chleb 4.69, mydlo 4.59, kurczak 24.19
- [x] `jajka` = 13.99 - po 185 dniach jako `-1`. Nigdy nie byly martwe, tylko czytane zlym selektorem
- [x] `lot` = 195.05 na 2026-09-09, po 988 dniach ciszy. Mediana z miesiaca przez publiczne API Ryanaira (`services-api.ryanair.com/farfnd/v4/oneWayFares/KRK/CIA/cheapestPerDay`), bez klucza, jeden request na dobe
- [x] `bigmac` i `aspiryna` przepisane na JSON-LD (`getJsonLD` + `szukajJsonLD`) - parsery poprawne, ale oba dostaja HTTP 403 z IP Mikrusa (patrz nizej)
- [x] Crontab naprawiony: `2 3 * * 5 /home/frog/zik/runGit.sh` - sciezka `home`, nie `homr`
- [x] Warstwowe komunikaty sie oplacily: w logu widac `jsonld [protokol] HTTP 403 dla https://www.wapteka.pl/...` zamiast dawnego "Problem z: aspiryna". Od razu wiadomo, ze parser jest OK a problem to dostep

## Znaleziska z logu produkcyjnego 2026-09-09
- [ ] `saveCSV` FAKTYCZNIE wprowadzil `\r\n`: piec nowych wierszy (2026-09-05..09) konczy sie `^M`, a 1030 historycznych na `\n`. Przewidziane 2026-09-04, teraz potwierdzone w danych. Poprawka: `open('zikDB.csv','a', newline='')` ORAZ `csv.DictWriter(..., lineterminator='\n')` - samo `newline=''` nie wystarczy
- [ ] `buty` skoczyly 239 -> 259 -> 549 w dwa dni (06->07->08.09). Opis mowi "najtansze szpilki", URL ma `product_list_order=price`, ale `getPageClass(url,'price')` bierze PIERWSZA cene, niekoniecznie najtansza. Ten sam mechanizm co przy `frisco` i `prad` - parser zwraca liczbe, tylko nie te, o ktora prosisz. Sprawdzic zanim utrwali sie w szeregu
- [ ] `telefon` padl 2026-09-07 (bylo 3648, jest -1). W logu `'NoneType' object has no attribute 'get_text'` - selektor `main-price` przestal pasowac
- [ ] `wapteka.pl` i `ubereats.com` zwracaja HTTP 403 z IP Mikrusa, choc z laptopa dzialaja. Parsery sa dobre. Przyczyna prawdopodobnie: blokada zakresow centrow danych. Do rozwazenia: `NAGLOWKI` wysylaja `Accept: text/html` i `Sec-Fetch-Dest: document` do endpointow zwracajacych JSON - prawdziwa przegladarka wysyla te naglowki tylko przy nawigacji, wiec z IP serwerowni to rozpoznawalny wzorzec
- [ ] `webmaker.sh` dopisuje log do samego siebie: `runZik.sh` przekierowuje stdout do `zikLast.log`, a potem podaje ten sam plik webmakerowi jako wejscie. Efekt: caly przebieg widnieje w logu DWA razy z identyczna mikrosekunda, a `zikFull.log` puchnie podwojnie. NIE jest to podwojny insert - `git diff` pokazuje po jednym wierszu na dzien. Poprawka: `webmaker.sh ... >/dev/null 2>&1`
- [ ] `runZik.sh`: `echo "BLAD: brak katalogu repo"` jest PRZED `exec`, wiec pod cronem idzie do maila, nie do logu. Ta sama pulapka co w `runGit.sh` - przeniesc `exec` nad `cd`
- [ ] Liczby inflacji w logu sa bezwartosciowe i wiadomo dlaczego: `chleb` +887% (porownanie smiecia 0.95 z czerwca 2025 z cena z dzis), `jajka` -108% i `piwo` -112% (bo `nowe = -1` wchodzi do wzoru jako liczba). Rozwiazuja to dwie otwarte pozycje: przeliczenie historycznych danych frisco oraz obsluga `nowe < 0` w `inflacja.py`. Do tego czasu rozwazyc wylaczenie tych printow, zeby nie sugerowaly wiarygodnosci
- [ ] Martwych pozycji: 10/33 (bylo 13). Zostaly: piwo, auto_Mean, auto_Median, telefon, bigmac, m2wtorny, m2pierwotny, fryzjer, upc, aspiryna, kasjer

## Zrobione 2026-09-09 (cd.)
- [x] `zajecia` w logu WYJASNIONE: `webmaker.sh:25-27` ma zmienna `zajecia` (nazwa po innym projekcie) trzymajaca tresc loga i debugowy `echo "zajecia $zajecia"`. `runZik.sh` przekierowuje stdout do `zikLast.log`, wiec webmaker dopisuje log do samego siebie. `tail -n +2 | head -n -1` tlumaczy, dlaczego kopia nie ma pierwszej i ostatniej linii. Dzieje sie od 2024-08-07, **1269 razy** (2024: 152, 2025: 361, 2026: 747). NIE bylo podwojnego insertu - `git diff` pokazuje po jednym wierszu na dzien
- [ ] Poprawka: usunac `echo` z `webmaker.sh:27` (pozostalosc po debugowaniu, `$zajecia` jest uzyte w linii 64 tam, gdzie ma byc). Alternatywnie `webmaker.sh ... >/dev/null 2>&1` w `runZik.sh`
- [ ] `zikFull.log` jest od dwoch lat dwa razy wiekszy niz powinien. Po poprawce warto rozwazyc przepisanie go bez duplikatow - w historii sa slady starych awarii warte archeologii, m.in. `<<<<<<< Updated upstream` (nierozwiazany konflikt gita w pliku .py, ktory Python probowal wykonac) i tracebacki z `zik.py line 14`
- [x] `telefon` naprawiony 2026-09-09 przez PODMIANE PRODUKTU (commit `54bf4c8`). Stary URL zwracal "Ten produkt jest niedostepny", a `.price` pokazywalo 179/247 zl (akcesoria). Stary parser szukal `main-price`, ktorego tam nie bylo, wiec zwracal `-1` - zepsul sie w najbezpieczniejszy mozliwy sposob. Nowy produkt: Samsung Galaxy S26 Ultra 256GB, cena 4253, klasa `main-price` dziala

## Zmiany produktu - do zapisania w tabeli (pozycja z TODO od 2026-08-31)
- [ ] `telefon`: do 2026-09-06 Samsung Galaxy S25 Ultra 256GB (ostatnia cena 3648) | od 2026-09-09 Samsung Galaxy S26 Ultra 256GB (pierwsza cena 4253). SKOK +16.6% NIE jest inflacja, to nowszy model. Definicja "Najlepszy flagowiec Samsunga" taka podmiane dopuszcza, ale trzeba wiedziec, ze ta kolumna mierzy "cene najnowszego flagowca", nie "cene tego samego telefonu w czasie"
- [ ] `piwo`: pid 3192 -> pid 153955 (ten sam produkt, 2 l, zmiana ID we Frisco)
- [ ] `aspiryna`: URL `/aspirin-500-mg-10-tabletek-2621,p` -> `/produkt/aspirin-10-tabl,3795/` (ten sam produkt)
- [ ] `lot`: do 2020-05-06 cena konkretnego dnia (12 odczytow: 77, 78, 82) | od 2026-09-09 MEDIANA z miesiaca. Nieporownywalne - stare 12 odczytow oznaczyc `-1`

## Historia kolumny telefon jest niewiarygodna (2026-09-09)
- [ ] 62 skoki powyzej 10% na 888 dodatnich odczytow. Trzy rodzaje smiecia: ceny akcesoriow (119, 130, 160, 453, 542 zl), ceny x100 (638900, 664900, 549900 - zgubiony separator dziesietny), oraz oscylacje 3598 <-> 7998 z dnia na dzien (rozne warianty pamieci)
- [ ] W odroznieniu od `frisco` NIE MA tu stalego przelicznika do przeliczenia wstecz. Trzeba by recznie ocenic, ktore odczyty sa wiarygodne - albo uznac kolumne za uzyteczna dopiero od 2026-09-09

## REGRESJA 2026-09-10: frisco padlo 8 z 9 na Mikrusie
- [ ] PILNE: run z 2026-09-10 02:02 zwrocil `-1` dla pizza, maslo, jablka, makaron, chleb, mydlo, kurczak, jajka, piwo. Przeszedl TYLKO `kielecki` (pierwszy frisco w koszyku). Dzien wczesniej wszystkie 9 dzialalo
- [ ] Przyczyna NIE jest parserem ani limitem szybkosci - sprawdzone:
  - laptop, 30 requestow: 30/30 nowy wariant
  - laptop, seria 10 bez przerw (jak `skanujKoszyk`): 9/10 nowy, brak degradacji w miare serii
  - laptop, `piwo` teraz: 1/1 nowy, w 10 probach NIE udalo sie trafic starego wariantu (wczesniej 3/8)
  - Mikrus 2026-09-09: 9/9 nowy | Mikrus 2026-09-10: 1/9
  Wniosek: decyduje KLIENT (adres IP), i zmienia sie w czasie. Wariant nie jest przypiety na stale
- [ ] To TRZECI serwis w tym tygodniu obslugujacy Mikrusa gorzej niz laptopa: `wapteka.pl` (403 vs 200), `ubereats.com` (403), `frisco.pl` (stary wariant vs nowy). Wspolny mianownik: adres w centrum danych. Problem przesunal sie z "kod czyta zle" na "serwis nas nie chce"
- [x] PONOWIENIE zrobione w `zik.py` (`skanujKoszyk`): jedna dodatkowa proba z `sleep(3)`, gdy `frisco()` zwroci -1
- [ ] KOREKTA 2026-09-10: rada "najwyzej 3 razy" byla ZLA. Pomiar: `piwo`, 40 prob w ~2.5 minuty -> 0 sukcesow, przy pojedynczym requescie pol godziny wczesniej -> sukces. Ponawianie tego samego URL zamienia awarie przelotna w TRWALA. Po serii `kielecki` i `chleb` dzialaly dalej, wiec blokada jest NA URL, nie na IP. Ten sam mechanizm co obrona antybotowa Ubera przy testach `bigmac`, tylko na poziomie jednego adresu
- [ ] JEDNA proba z przerwa to bezpieczny sufit. NIE podnosic
- [ ] Pulapka metodologiczna do zapamietania: test 40 requestow prawdopodobnie SAM wywolal wynik, ktory zmierzyl. Nie da sie dzis odroznic "piwo trwale dostaje stary wariant" od "moje probki zablokowaly ten URL". Zmierzyc ponownie po dobie
- [ ] `piwo` NIE naprawi sie ponowieniem - potrzebny inny produkt (inne `pid` czteropaku Zywca we Frisco) albo inny sklep. To decyzja o zrodle, nie o kodzie
- [ ] Hipoteza do sprawdzenia: `piwo` jest jedynym alkoholem wsrod produktow frisco i jedynym trwale degradowanym. Polskie prawo ogranicza reklame alkoholu, a wariant bez ceny to dokladnie to, co zrobilby serwis dzialajacy ostroznie. Wczesniej nie znalazlem markerow weryfikacji wieku, ale 3/8 i potem 0/44 pasuje do reguly stosowanej niekonsekwentnie. Test rozstrzygajacy: wziac dowolny INNY alkohol z frisco i sprawdzic, czy tez dostaje stary wariant

## Zrobione 2026-09-10
- [x] `saveCSV` naprawione: `open(...,'a', newline='')` + `csv.DictWriter(..., lineterminator='\n')`. Nowe wiersze beda mialy `\n`
- [ ] Zostaje jednorazowe posprzatanie 5 wierszy z `^M` (2026-09-05..09): `sed -i 's/\r$//' zikDB.csv` na Mikrusie
- [x] `frisco` potwierdzone z laptopa 2026-09-10: 9 z 10 produktow zwraca ceny (kielecki 14.19, pizza 11.09, maslo 5.89, jablka 6.49, makaron 5.19, chleb 4.69, mydlo 4.59, kurczak 24.19, jajka 13.99). Wczorajsza regresja byla przelotna

  - limit prob musi byc twardy: `timeout=15` chroni JEDEN request, nie petle
  - `time.sleep` jest obowiazkowy: ponawianie bez przerwy wywolalo obrone antybotowa Ubera przy testach `bigmac`
  - umiescic w osobnej funkcji pomocniczej (np. "pobierz element o tej klasie, ponawiajac N razy"), bo `kazar` (`buty`) tez dzis padl i prawdopodobnie ma ten sam problem
- [ ] NIE wyliczac ceny ze starego wariantu (cena za kg x pojemnosc). Kusi, bo dane tam sa, ale w 10 probach nie udalo sie trafic starego wariantu - czyli tej sciezki NIE DA SIE przetestowac. Kod nietestowalny, wykonywany raz na kilka tygodni, to dokladnie miejsce, gdzie w tej sesji czterokrotnie znajdowalismy bledy
- [ ] `buty` (kazar) tez padl 2026-09-10, ale w logu jest samo "Problem z: buty" bez zadnego komunikatu - bo `kazar()` ma gole `except:`. Nie wiadomo, czy to stary wariant, 403, czy cos innego. Konkretny koszt jednego z 13 otwartych golych `except:`
- [ ] FOOD Inflantion skoczyla do 274.8% (dzien wczesniej 95.2%) - bo osiem pozycji spozywczych weszlo do wzoru jako `nowe = -1`. Kolejny dowod, ze `inflacja.py` musi obslugiwac `nowe < 0`

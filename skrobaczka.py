# coding=utf-8
#! python3
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import funkcyjki as f
import statistics
import json
import datetime
import os
from koszyk import getProduct
import pathlib

ENV = pathlib.Path(__file__).resolve().parent / '.env'
NAGLOWKI = {
      'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
      'Accept-Language': 'pl-PL,pl;q=0.9,en;q=0.8',
      'Accept-Encoding': 'gzip, deflate',
      'Upgrade-Insecure-Requests': '1',
      'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate',
      'Sec-Fetch-Site': 'none', 'Sec-Fetch-User': '?1',
}

def wczytajEnv(sciezka=ENV):
	"""Wczytuje zmienne z .env lezacego obok tego pliku.

	Sciezka liczona od __file__, nie od CWD - cron startuje w $HOME.
	Nie nadpisuje zmiennych juz obecnych w srodowisku, wiec da sie
	podmienic klucz na czas testu: FIXER_API_KEY=inny python3 zik.py
	"""
	if not sciezka.exists():
		return
	for linia in sciezka.read_text(encoding='utf-8').splitlines():
		linia = linia.strip()
		if not linia or linia.startswith('#'):
			continue
		if linia.startswith('export '):
			linia = linia[len('export '):]
		klucz, znak, wartosc = linia.partition('=')
		if not znak:
			continue
		os.environ.setdefault(klucz.strip(), wartosc.strip().strip('\'"'))

wczytajEnv()

def waluty():
	fixer_api_key = os.environ.get('FIXER_API_KEY')
	if not fixer_api_key:
		raise RuntimeError(f'brak FIXER_API_KEY - sprawdz {ENV}')
	url = f"https://data.fixer.io/api/latest?access_key={fixer_api_key}&symbols=USD,PLN,XAU,CHF"

	# warstwa 1: TRANSPORT - siec, DNS, timeout.
	try:
		response = requests.get(url, timeout=15)
	except requests.RequestException as e:
		raise RuntimeError(f'fixer.io [transport]: {type(e).__name__}') from None

	# warstwa 2: PROTOKOL - HTTP 4xx/5xx nie rzuca samo z siebie.
	if response.status_code != 200:
		raise RuntimeError(f'fixer.io [protokol] HTTP {response.status_code}')

	# warstwa 3: FORMAT - cialo moze nie byc JSON-em (strona techniczna, proxy).
	try:
		parsed = json.loads(response.text)
	except ValueError:
		raise RuntimeError(f'fixer.io [format] nie JSON: {response.text[:80]!r}') from None

	# warstwa 4a: TRESC - fixer zglasza blad przez success:false (np. limit API).
	if not parsed.get('success'):
		raise RuntimeError(f'fixer.io [tresc] blad API: {parsed.get("error")}')

	# warstwa 4b: TRESC - brakujace lub zerowe kursy. "not rates.get(s)" lapie
	rates = parsed.get('rates') or {}
	brakujace = [s for s in ('PLN', 'USD', 'XAU', 'CHF') if not rates.get(s)]
	if brakujace:
		raise RuntimeError(f'fixer.io [tresc] brak lub zerowe kursy: {brakujace}')

	pln = float(rates['PLN'])
	return {'eur': pln,
			'xau': pln/float(rates['XAU']),
			'chf': pln/float(rates['CHF']),
			'usd': pln/float(rates['USD'])}


def bigmac(url):
	try:
		pozycje = szukajJsonLD(getJsonLD(url), 'MenuItem')
		if not pozycje:
			raise ValueError('jsonld [tresc] brak pozycji MenuItem')
		trafienia = [p for p in pozycje if p.get('name') == 'Big Mac®']
		if not trafienia:
			podobne = sorted({p.get('name','') for p in pozycje if 'Mac' in p.get('name','')})
			raise ValueError(f'jsonld [tresc] brak pozycji "Big Mac®" wsrod {len(pozycje)}; podobne: {podobne}')
		of = trafienia[0].get('offers')
		if isinstance(of, list):
			of = of[0] if of else None
		if not isinstance(of, dict):
			raise ValueError(f'jsonld [tresc] "Big Mac®" bez oferty: offers={of!r}')
		cena = of.get('price')
		if not cena:
			raise ValueError(f'jsonld [tresc] "Big Mac®" bez ceny: oferta={of!r}')
		return f.zrobCene("bigmac",cena)
	except Exception as e:
		print(e)
		return float(-1)

def getJsonLD(url, headers=None):
	page = requests.get(url, headers=headers or NAGLOWKI, timeout=15)
	if page.status_code != 200:
		raise RuntimeError(f'jsonld [protokol] HTTP {page.status_code} dla {url[:60]}')
	soup = BeautifulSoup(page.content, 'html.parser')
	if soup.head is None or soup.head.title.get_text(strip=True) == "":
		raise RuntimeError(f'jsonld [antybot]  dla {url[:60]}')
	encje = []
	for tag in soup.find_all('script', type='application/ld+json'):
		try:
			dane = json.loads(tag.get_text())
		except ValueError:
			continue                                   # zepsuty blok pomijamy
		if isinstance(dane, list):
			encje.extend(dane)                         # kształt 2
		elif isinstance(dane, dict) and '@graph' in dane:
			encje.extend(dane['@graph'])               # kształt 3
		else:
			encje.append(dane)                         # kształt 1 - tu append je
	return encje

def szukajJsonLD(dane, typ):
	znalezione = []
	def przejdz(obiekt):
		if isinstance(obiekt, dict):
			tp = obiekt.get('@type')
			if tp == typ or (isinstance(tp, list) and typ in tp):
				znalezione.append(obiekt)
			for wartosc in obiekt.values():
				przejdz(wartosc)
		elif isinstance(obiekt, list):
			for wartosc in obiekt:
				przejdz(wartosc)
	przejdz(dane)
	return znalezione

def getPage(url):
	page = requests.get(url, timeout=15)
	soup = BeautifulSoup(page.content, 'html.parser')
	return soup.prettify()
	# return str(urlopen(url).read())

def getPageHeader(url,header):
	page = requests.get(url,headers=header, timeout=15)
	soup = BeautifulSoup(page.content, 'html.parser')
	return str(soup)

def printPageHeader(url,header):
	page = requests.get(url,headers=header, timeout=15)
	soup = BeautifulSoup(page.content, 'html.parser')
	text_file = open("s.html", "w")
	text_file.write(soup.prettify())
	text_file.close()

def printPage(url):
	page = requests.get(url, timeout=15)
	soup = BeautifulSoup(page.content, 'html.parser')
	text_file = open("s.html", "w")
	text_file.write(soup.prettify())
	text_file.close()

def getPageClass(url,klasa):
	headers = requests.utils.default_headers()
	headers.update(NAGLOWKI)
	page = requests.get(url,headers=headers, timeout=15)
	soup = BeautifulSoup(page.content, 'html.parser')
	return soup.find(class_=klasa)

def getPageClassAll(url,klasa):
	headers = requests.utils.default_headers()
	headers.update(NAGLOWKI)
	page = requests.get(url,headers=headers, timeout=15)
	soup = BeautifulSoup(page.content, 'html.parser')
	return soup.find_all(class_=klasa)

def getPageId(url,idx):
	page = requests.get(url, timeout=15)
	soup = BeautifulSoup(page.content, 'html.parser')
	return soup.find(id=idx)

def otomoto(url):
	rok = str(int(datetime.date.today().year)-3)
	url = url.replace("2018",rok)
	try:
		stron = int(getPageClassAll(url,'pagination-item ooa-1xgr17q')[-1].get_text())
		kwota = []
		for i in range(1,stron):
			car = getPageClassAll(url+'&page='+str(i),'efpuxbr16 ooa-1n2paoq er34gjf0')
			for x in car:
				cenaAuta = x.get_text().replace("\n", "")
				if ("Miesiąc" in cenaAuta):
					continue
				if ("," in cenaAuta):
					cenaAuta = cenaAuta[:cenaAuta.find(",")]
				nowacenaAuta = ''.join(z for z in cenaAuta if z.isdigit())
				if(nowacenaAuta==""):
					continue
				nowacenaAutaF = float(nowacenaAuta)
				kwota.append(float(nowacenaAuta))
		print('Ofert aut: ',len(kwota))
		return [f.zrobCene("otomoto",statistics.mean(kwota)),f.zrobCene("otomoto",statistics.median(kwota))]
	except Exception as e:
		print(e)
		print ("Problem z: otomoto")
		return [float(-1),float(-1)]

def frisco(url):
	try:
		cena = getPageClass(url,'f-pdp__price-amount--emphasized').get_text()
		return f.zrobCene("frisco",cena)
	except Exception as e:
		print(e)
		print ("Problem z: ",getProduct(url))
		return float(-1)

def kazar(url):
	try:
		cena = getPageClass(url,'price').get_text().replace(",-","")
		return f.zrobCene("kazar",cena)
	except:
		print ("Problem z: ",getProduct(url))
		return float(-1)

def fryzjer(url):
	try:
# curl 'https://www.rezerwacje-jeanlouisdavid.pl/api/salon-prices/M58'  -H 'X-API-Version: 4' -H 'X-Client-Name: web' -H 'X-Brand: JLD' -H 'Referer: https://www.rezerwacje-jeanlouisdavid.pl/salons/Krakow/C.H.Krokus/M58' -H 'Cookie: permuserid=2111191QU9UIHIVW0HKQLUIHMDOYNNIC; _gcl_au=1.1.498805932.1637337375; _ga_K358R1KWGB=GS1.1.1637337374.1.0.1637337384.50; _ga=GA1.2.734974029.1637337376; _gid=GA1.2.1895826946.1637337377; _dc_gtm_UA-46770041-1=1; _dc_gtm_UA-46770041-3=1; _gat_UA-46770041-1=1; _fbp=fb.1.1637337377808.841734507'
		headers = {
			'X-API-Version': '4',
			'X-Client-Name': 'web',
			'X-Brand': 'JLD',
			'Referer': 'https://www.rezerwacje-jeanlouisdavid.pl/salons/Krakow/C.H.Krokus/M58',
			'Cookie': 'permuserid=2111191QU9UIHIVW0HKQLUIHMDOYNNIC; _gcl_au=1.1.498805932.1637337375; _ga_K358R1KWGB=GS1.1.1637337374.1.0.1637337384.50; _ga=GA1.2.734974029.1637337376; _gid=GA1.2.1895826946.1637337377; _dc_gtm_UA-46770041-1=1; _dc_gtm_UA-46770041-3=1; _gat_UA-46770041-1=1; _fbp=fb.1.1637337377808.841734507',
			}
		ceny = getPageHeader(url,headers)
		gdzie = ceny.find("Mycie z masażem, strzyżenie")
		return f.zrobCene("fryzjer",ceny[gdzie+37:gdzie+42])
	except:
		print ("Problem z: ",getProduct(url))
		return float(-1)

def prad(url):
	try:
		kod = getPage(url)
		cena = kod.find('#0070C0')
		kwota = kod[cena+8:cena+30]
		return f.zrobCene("prad",kwota)
	except:
		print ("Problem z: ",getProduct(url))
		return float(-1)

def auchan(url):

	try:
		page = requests.get(url, timeout=15)
		kod = BeautifulSoup(page.content, 'html.parser')
		kod = kod.get_text()
		cena = kod.find('product_unitprice_ati')
		kwota = kod[cena+23:cena+50]
		kwota = kwota[:kwota.find(',')]
		return f.zrobCene("auchan",kwota)
	except:
		print ("Problem z: ",getProduct(url))
		return float(-1)

def m2(url):
	try:
		kod = getPage(url)

		cena = kod.rfind("data-v-f02966ee")
		kwota = kod[cena:cena+100]
		beg = kwota.find('(')+1
		kwota = kwota[beg:beg+7]

		return f.zrobCene("m2",kwota)
	except Exception as e:
		print(e)
		print ("Problem z: ",getProduct(url))
		return float(-1)


def karma(url):
	try:
		kwota = getPageClassAll(url,'price__value price__value_bold js__price-value')[1].get_text()
		return f.zrobCene("karma",kwota)
	except:
		print ("Problem z: ",getProduct(url))
		return float(-1)

def aspiryna(url):
	try:
		produkt = None
		for encja in getJsonLD(url):
			tp = encja.get('@type')
			if tp == 'Product' or (isinstance(tp, list) and 'Product' in tp):
				produkt = encja
				break
		if produkt is None:
			raise ValueError('brak encji Product w JSON-LD')
		of = produkt.get('offers')
		if isinstance(of, list):
			of = of[0]
		cena = of.get('price')
		return f.zrobCene("aspiryna",cena)
	except Exception as e:
		print(e)
		print ("Problem z: ",getProduct(url))
		return float(-1)

def rolex(url):
	try:
		cena = getPageClass(url,'price dig').get_text()
		cena = cena[:cena.find('z')]
		return f.zrobCene("rolex",cena)
	except:
		print ("Problem z: ",getProduct(url))
		return float(-1)

def benzyna(url):
	return f.zrobCene("benzyna",getPageClass(url,'price').get_text())

def kindl(url):
	try:
		return f.zrobCene("kindle",getPageClass(url,'h2 price').get_text())
	except:
		print ("Problem z: ",getProduct(url))
		return float(-1)

def kasjer(url):
	try:
		return f.zrobCene("kasjer",getPageClass(url,'salary-info-value').get_text())
	except:
		print ("Problem z: ",getProduct(url))
		return float(-1)

def alkohol(url):
	try:
		kwota = getPageClassAll(url,'price')[1].get_text()
		return f.zrobCene("alkohol",kwota)
	except:
		print ("Problem z: ",getProduct(url))
		return float(-1)

def spolem(url):
	try:
		kwota = getPageClassAll(url,'woocommerce-Price-amount amount')[3].get_text()
		return f.zrobCene("spolem",kwota)
	except:
		print ("Problem z: ",getProduct(url))
		return float(-1)

def lot(url):
	try:
		miesiac = ((datetime.date.today()+datetime.timedelta(days=90))).replace(day=1)
		params = {'outboundMonthOfDate': miesiac.isoformat(),
						'currency': 'PLN',
						'market': 'pl-pl'}
		try:
			response = requests.get(url, headers=NAGLOWKI, timeout=15, params=params)
		except requests.RequestException as e:
			raise RuntimeError(f'ryanair [transport]: {type(e).__name__}') from None
		if response.status_code != 200:
			raise RuntimeError(f'ryanair [protokol] HTTP {response.status_code}')
		try:
			r = json.loads(response.text)
		except ValueError:
			raise RuntimeError(f'ryanair [format] nie JSON: {response.text[:80]!r}') from None
		loty = r["outbound"]["fares"]
		ceny =[]
		for l in loty:
			if l.get('price') is None:
				continue
			ceny.append(l['price']['value'])
		# print(lot)

		return f.zrobCene("lot",statistics.median(ceny))


	except Exception as e:
		print(e)
		print ("Problem z: ",getProduct(url))
		return float(-1)

def upc(url):
		try:
			strona = getPage(url)
			kwota = strona.find('v-rich-text__old-price')
			strona=strona[kwota:kwota+100]
			kwota = strona.find('003E')
			return f.zrobCene("upc",strona[kwota+4:kwota+6])
		except:
			print ("Problem z: ",getProduct(url))
			return float(-1)


def telefon(url):
	try:
		cena =  getPageClass(url,'main-price').get_text()
		# cena = cena.replace(" ", "")
		return f.zrobCene("telefon",cena)
	except Exception as e:
		print(e)
		print ("Problem z: ",getProduct(url))
		return float(-1)

def lekarz(url):
	try:
		lek = getPageClassAll(url,'m-0 text-nowrap font-weight-bold')
		kwota = []
		for x in lek:
			# print("####",x,"####")
			x = x.get_text()[20:].strip()
			# print("@@@@@",x,"@@@@")
			kwota.append(f.zrobCene("lekarz",x))
		return [f.zrobCene("lekarz",statistics.mean(kwota)),f.zrobCene("lekarz",statistics.median(kwota))]
	except Exception as e:
		print(e)
		print ("Problem z: ",getProduct(url))
		return [float(-1),float(-1)]

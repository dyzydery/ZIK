# coding=utf-8
#! python3
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import funkcyjki as f
import statistics
import json
import datetime

def waluty():
	# Key Fixerio 82115c700a7d9d17d383a6f386a67a92
	# http://data.fixer.io/api/latest?access_key=82115c700a7d9d17d383a6f386a67a92
	url = "http://data.fixer.io/api/latest?access_key=82115c700a7d9d17d383a6f386a67a92&symbols=USD,PLN,XAU,CHF"
	response = requests.get(url)
	data = response.text
	parsed = json.loads(data)
	pln = parsed["rates"]["PLN"]
	usd = parsed["rates"]["USD"]
	xau = parsed["rates"]["XAU"]
	chf = parsed["rates"]["CHF"]
	return {'eur':float(pln),
			'xau':float(pln)/float(xau),
			'chf':float(pln)/float(chf),
			'usd':float(pln)/float(usd)}

def bigmac(url):
	try:
		header = {'accept' : 'text/html'}
		kod = getPageHeader(url,header)
		cena = kod.find("Big Mac®\"")
		kwota = kod[cena+62:cena+67]
		# print("bigmac:", kwota)
		return kwota
	except Exception as e:
		print(e)
		print ("Problem z: ",url)
		return '-1'


def getPage(url):
	return str(urlopen(url).read())

def getPageHeader(url,header):
	page = requests.get(url,headers=header)
	soup = BeautifulSoup(page.content, 'html.parser')
	return str(soup)

def printPageHeader(url,header):
	page = requests.get(url,headers=header)
	soup = BeautifulSoup(page.content, 'html.parser')
	text_file = open("s.html", "w")
	text_file.write(soup.prettify())
	text_file.close()

def printPage(url):
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	text_file = open("s.html", "w")
	text_file.write(soup.prettify())
	text_file.close()

def getPageClass(url,klasa):
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	return soup.find(class_=klasa)

def getPageClassAll(url,klasa):
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	return soup.find_all(class_=klasa)

def getPageId(url,idx):
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	return soup.find(id=idx)

def otomoto(url):
	rok = str(int(datetime.date.today().year)-3)
	url = url.replace("2018",rok)
	try:
		stron = int(getPageClassAll(url,'ooa-xdlax9 eesa4ha0')[-1].get_text())
		kwota = []
		for i in range(1,stron):
			car = getPageClassAll(url+'&page='+str(i),'ooa-1bmnxg7 e1p19lg711')
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
		return [statistics.mean(kwota),statistics.median(kwota)]
	except Exception as e:
		print(e)
		print("problem z: ", url)
		return [-1.0,-1.0]


def carrefour(rzecz,url):
	try:

		if (rzecz=='jablka' or rzecz=='jajka' or rzecz=='kurczak'):
			kwota = getPageClassAll(url,'MuiTypography-root MuiTypography-caption MuiTypography-colorTextSecondary')[1]
			kwota = kwota.get_text()
			kwota = kwota[0:kwota.find("zł")]
		else:
			kwota1 = getPageClass(url,'MuiTypography-root jss133 MuiTypography-h1').get_text()
			kwota2 = getPageClass(url,'MuiTypography-root jss133 jss189 MuiTypography-h3').get_text()
			kwota = kwota1+','+kwota2
		return kwota
	except Exception as e:
		print(e)
		print("problem z: ", url)
		return '-1'

def kazar(url):
	try:
		cena = getPageClass(url,'price').get_text().replace(",-","")
		return cena
	except:
		print("problem z: ", url)
		return '-1'

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
		return ceny[gdzie+37:gdzie+42]
	except:
		print("problem z: ", url)
		return '-1'

def prad(url):
	try:
		kod = getPage(url)
		cena = kod.find('mso-highlight:yellow')
		kwota = kod[cena+23:cena+27]
		return kwota
	except:
		print("problem z: ", url)
		return '-1'

def auchan(url):

	try:
		page = requests.get(url)
		kod = BeautifulSoup(page.content, 'html.parser')
		kod = kod.get_text()
		cena = kod.find('product_unitprice_ati')
		kwota = kod[cena+23:cena+50]
		kwota = kwota[:kwota.find(',')]
		return kwota
	except:
		print("problem z: ", url)
		return '-1'

def m2(url):
	kwota = getPageId(url,'locationPageLink').get_text()
	kwota = kwota[kwota.find('(')+1:kwota.find('zł/m')]
	return kwota

def karma(url):
	try:
		return getPageClass(url,'main-price color').get_text()
	except:
		print("problem z: ", url)
		return '-1'

def aspiryna(url):
	try:
		cena = getPageClass(url,'col-3 col-lg-1 align-self-center fw-bold text-center').get_text()#.strip()
		return cena
	except:
		print("problem z: ", url)
		return '-1'

def rolex(url):
	try:
		return getPageClass(url,'price dig').get_text()
	except:
		print("problem z: ", url)
		return '-1'

def benzyna(url):
	return getPageClass(url,'price').get_text()

def kindl(url):
	try:
		return getPageClass(url,'value').get_text()
	except:
		print("problem z: ", url)
		return '-1'

def kasjer(url):
	try:
		return getPageClass(url,'salary-info-value').get_text()
	except:
		print("problem z: ", url)
		return '-1'

def alkohol(url):
	try:
		kwota = getPageId(url,'our_price_display').get_text()
		return kwota
	except:
		print("problem z: ", url)
		return '-1'

def spolem(url):
	try:
		kwota = getPageClassAll(url,'woocommerce-Price-amount amount')[3].get_text()
		return kwota
	except:
		print("problem z: ", url)
		return '-1'

def lot(url):
	try:
		data = str(datetime.date.today()+datetime.timedelta(days=90))
		return getPageClass(url+data,' length-5').get_text()
	except:
		print("problem z: ", url)
		return '-1'

def upc(url):
		try:
			kwota = getPageClass(url,'lgi-hdr-9 ph2-d l-h6 m-h0 lgi-txtsd-default').get_text()
			lok = kwota.find('zł/mies')
			kwota = kwota[lok-6:lok]
			return kwota
		except:
			print("problem z: ", url)
			return '-1'


def telefon(url):
	try:
		return getPageClass(url,'price-normal').get_text()
	except:
		print("problem z: ", url)
		return '-1'

def lekarz(url):
	try:
		lek = getPageClassAll(url,'m-0 text-nowrap font-weight-bold')
		kwota = []
		for x in lek:
			# print("####",x,"####")
			x = x.get_text()[20:].strip()
			# print("@@@@@",x,"@@@@")
			kwota.append(f.zrobCene(x))
		return [statistics.mean(kwota),statistics.median(kwota)]
	except Exception as e:
		print(e)
		print("problem z: ", url)
		return [float(-1),float(-1)]

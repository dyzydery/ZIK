# coding=utf-8
#! python3
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import funkcyjki as f
import statistics
import json
import datetime
from koszyk import getProduct

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
		if cena==-1:
			raise
		kwota = kod[cena+62:cena+67]
		# print("bigmac:", kwota)
		return f.zrobCene(kwota)
	except Exception as e:
		#print(e)
		print ("Problem z: BigMac")
		return float(-1)


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
	headers = requests.utils.default_headers()
	headers.update({
	    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 OPR/100.0.0.0',
	})
	page = requests.get(url,headers=headers)
	soup = BeautifulSoup(page.content, 'html.parser')
	return soup.find(class_=klasa)

def getPageClassAll(url,klasa):
	headers = requests.utils.default_headers()
	headers.update({
	    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 OPR/100.0.0.0',
	})
	page = requests.get(url,headers=headers)
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
		return [f.zrobCene(statistics.mean(kwota)),f.zrobCene(statistics.median(kwota))]
	except Exception as e:
		print(e)
		print ("Problem z: ",getProduct(url))
		return [float(-1),float(-1)]

def frisco(url):
	try:
		main = getPageClassAll(url,'price_num')[-1].get_text()
		decim = getPageClassAll(url,'price_decimals')[-1].get_text()
		cena = main+'.'+decim
		if(cena=="0.00"):
			print ("Problem z: ",getProduct(url))
			return float(-1)
		# print (cena)
		return f.zrobCene(cena)
	except Exception as e:
		print(e)
		print ("Problem z: ",getProduct(url))
		return float(-1)

def kazar(url):
	try:
		cena = getPageClass(url,'price').get_text().replace(",-","")
		return f.zrobCene(cena)
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
		return f.zrobCene(ceny[gdzie+37:gdzie+42])
	except:
		print ("Problem z: ",getProduct(url))
		return float(-1)

def prad(url):
	try:
		kod = getPage(url)
		cena = kod.find('/kWh')
		kwota = kod[cena-10:cena-5]
		return f.zrobCene(kwota)
	except:
		print ("Problem z: ",getProduct(url))
		return float(-1)

def auchan(url):

	try:
		page = requests.get(url)
		kod = BeautifulSoup(page.content, 'html.parser')
		kod = kod.get_text()
		cena = kod.find('product_unitprice_ati')
		kwota = kod[cena+23:cena+50]
		kwota = kwota[:kwota.find(',')]
		return f.zrobCene(kwota)
	except:
		print ("Problem z: ",getProduct(url))
		return float(-1)

def m2(url):
	try:
		kwota = getPageClass(url,'aAre96').get_text()
		kwota = kwota[kwota.find('(')+1:kwota.find('zł/m')]
		return f.zrobCene(kwota)
	except:
		print ("Problem z: ",getProduct(url))
		return float(-1)


def karma(url):
	try:
		return f.zrobCene(getPageClass(url,'main-price').get_text())
	except:
		print ("Problem z: ",getProduct(url))
		return float(-1)

def aspiryna(url):
	try:
		cena = getPageClass(url,'col-3 col-lg-1 align-self-center fw-bold text-center').get_text()#.strip()
		return f.zrobCene(cena)
	except:
		print ("Problem z: ",getProduct(url))
		return float(-1)

def rolex(url):
	try:
		cena = getPageClass(url,'price dig').get_text()
		cena = cena[:cena.find('z')]
		return f.zrobCene(cena)
	except:
		print ("Problem z: ",getProduct(url))
		return float(-1)

def benzyna(url):
	return f.zrobCene(getPageClass(url,'price').get_text())

def kindl(url):
	try:
		return f.zrobCene(getPageClass(url,'h2 price').get_text())
	except:
		print ("Problem z: ",getProduct(url))
		return float(-1)

def kasjer(url):
	try:
		return f.zrobCene(getPageClass(url,'salary-info-value').get_text())
	except:
		print ("Problem z: ",getProduct(url))
		return float(-1)

def alkohol(url):
	try:
		kwota = getPageClassAll(url,'price')[1].get_text()
		return f.zrobCene(kwota)
	except:
		print ("Problem z: ",getProduct(url))
		return float(-1)

def spolem(url):
	try:
		kwota = getPageClassAll(url,'woocommerce-Price-amount amount')[3].get_text()
		return f.zrobCene(kwota)
	except:
		print ("Problem z: ",getProduct(url))
		return float(-1)

def lot(url):
	try:
		data = str(datetime.date.today()+datetime.timedelta(days=90))
		return f.zrobCene(getPageClass(url+data,' length-5').get_text())
	except:
		print ("Problem z: ",getProduct(url))
		return float(-1)

def upc(url):
		try:
			strona = getPage(url)
			kwota = strona.find('v-rich-text__old-price')
			strona=strona[kwota:kwota+100]
			kwota = strona.find('003E')
			return f.zrobCene(strona[kwota+4:kwota+6])
		except:
			print ("Problem z: ",getProduct(url))
			return float(-1)


def telefon(url):
	try:
		cena =  getPageClass(url,'main-price').get_text()
		# cena = cena.replace(" ", "")
		return f.zrobCene(cena)
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
			kwota.append(f.zrobCene(x))
		return [f.zrobCene(statistics.mean(kwota)),f.zrobCene(statistics.median(kwota))]
	except Exception as e:
		print(e)
		print ("Problem z: ",getProduct(url))
		return [float(-1),float(-1)]

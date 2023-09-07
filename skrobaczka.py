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

	Cookie = "SESSION=7896bb99-b689-487c-8492-844f1f0edcb6; GCLB=CM2Wu_C62cnXLQ; __cf_bm=JGxB7ulBrQSxd1UfHZrunK6oDdrnihTmWNAC1Zo0Fpo-1689935934-0-AbAtgePixWlokps/k3c99YRSqo8GPQbp+dS33Eve0lSNj8owc7PaW63dVsdqrJpYYmEq0HuCA7UoZo+AdBg9lWc=; cf_clearance=04Y8h221XF1Y68sFkylUvLsZurp2E3_IuyWh49FAv68-1689935934-0-0.2.1689935934; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Jul+21+2023+12%3A38%3A58+GMT%2B0200+(Central+European+Summer+Time)&version=6.35.0&isIABGlobal=false&hosts=&consentId=7e0c54d0-9e8d-4d1a-bd75-181af5b244a8&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0005%3A1%2CC0039%3A1%2CC0138%3A1%2CC0142%3A1%2CC0056%3A1%2CC0141%3A1%2CC0096%3A1%2CSTACK1%3A1%2CSTACK42%3A1; _snrs_sa=ssuid:85866b5f-eccd-43d6-93f0-8719230a4e28&appear:1689935937&sessionVisits:1; _snrs_sb=ssuid:85866b5f-eccd-43d6-93f0-8719230a4e28&leaves:1689935938; _snrs_p=host:www.carrefour.pl&permUuid:3e3e0279-5b47-4e51-b369-f6588a2ceb10&uuid:3e3e0279-5b47-4e51-b369-f6588a2ceb10&identityHash:&user_hash:&init:1689935937&last:1689935937&current:1689935937&uniqueVisits:1&allVisits:1; _snrs_uuid=3e3e0279-5b47-4e51-b369-f6588a2ceb10; _snrs_puuid=3e3e0279-5b47-4e51-b369-f6588a2ceb10; OptanonAlertBoxClosed=2023-07-21T10:38:58.408Z; eupubconsent-v2=CPvQM_APvQM_AAcABBENDPCsAP_AAH_AAChQJkNf_X__b2_r-_7_f_t0eY1P9_7__-0zjhfdl-8N3f_X_L8X52M5vF36tqoKuR4ku3bBIUdlHPHcTVmw6okVryPsbk2cr7NKJ7PEmlMbM2dYGH9_n9_z-ZKY7___f__z_v-v___9____7-3f3__5__--__e_V_-9zfn9_____9vP___9v-_9_3________3_79_7_D9-f_87_XQTHAJMNS4gC7IkZCbaMIoUQIwrCQqgUAFEAkLRAYQurgp2VwE-sBkAKEUATwQAhgBRkACAAASAJCIAJAjwQCAQCAQAAgAVCAQAMbAAPAC0EAgAFAdCxTigCUCwgyICIhTAhKkSCgnsqEEoP9BXCEOssCKDR_xUICNZAxWBEJCxchwRICXiSQPdUb4ACEAKAUSoViKT80BCgmbLVAAA.f_gAD_gAAAAA; _ga=GA1.2.1116619709.1689935939; _gid=GA1.2.1003232120.1689935939; _ga_J6DEHPJ090=GS1.1.1689935938.1.0.1689935939.59.0.0; _ga_NN2HTTVE2S=GS1.1.1689935938.1.0.1689935938.0.0.0; _fbp=fb.1.1689935939315.511211510"


	headers = requests.utils.default_headers()
	headers.update({
	    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
	    "Accept-Encoding": "gzip, deflate, br",
	    "Accept-Language": "en-US,en;q=0.5",
		"Connection": "keep-alive",
		"Sec-Fetch-Dest": "document",
	    "Sec-Fetch-Mode": "navigate",
		"Sec-Fetch-Site": "cross-site",
		"Upgrade-Insecure-Requests": "1",
	    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0",

	})
	page = requests.get(url,headers=headers)
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
		stron = int(getPageClassAll(url,'ooa-xdlax9 e1f09v7o0')[-1].get_text())
		kwota = []
		for i in range(1,stron):
			car = getPageClassAll(url+'&page='+str(i),'ev7e6t82 ooa-bz4efo er34gjf0')
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

def barbora(url):
	try:
		kwota = getPageClass(url,'b-product-price-current-number').get_text()
		if (url.find('jaja')!=-1):
			kwota = str(f.zrobCene(kwota)/10)
		return kwota
	except Exception as e:
		print(e)
		print("problem z: ", url)
		return '-1'

def piwo(url):
	try:
		page = getPage(url)
		x = page.find('/produkty/piwo-zywiec-4-x-500-ml-puszka')
		page = page[x:]
		kwota = page.find('itemprop="price"')
		page = page[kwota:]
		kwota = page.find('>')
		return page[kwota+3:kwota+30]
	except Exception as e:
		print(e)
		print("problem z: ", url)
		return '-1'


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
	try:
		kwota = getPageClass(url,'list-header__average-price').get_text()
		kwota = kwota[kwota.find('(')+1:kwota.find('zł/m')]
		return kwota
	except:
		print("problem z: ", url)
		return '-1'


def karma(url):
	try:
		return getPageClass(url,'main-price').get_text()
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
			strona = getPage(url)
			kwota = strona.find('v-rich-text__old-price')
			strona = strona[kwota:]
			kwota = strona.find('003E')
			return strona[kwota+4:kwota+7]
		except:
			print("problem z: ", url)
			return '-1'


def telefon(url):
	try:
		cena =  getPageClass(url,'price__value').get_text()
		cena = cena.replace(" ", "")
		return cena
	except Exception as e:
		print(e)
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

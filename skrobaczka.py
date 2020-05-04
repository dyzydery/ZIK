# coding=utf-8
#! python3
from bs4 import BeautifulSoup
from urllib.request import urlopen
import requests
import funkcyjki as f
import statistics
def getPage(url):
	return str(urlopen(url).read())

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

def tesco(rzecz,url):
	try:
		kwota = getPageClass(url,'value')
		if (rzecz=='jablka' or rzecz=='jajka' or rzecz=='kurczak'):
			kwota = getPageClass(url,'price-per-quantity-weight').find(class_='value')
		return kwota.get_text()
	except:
		print("problem z: ", url)
		return '0'

def kazar(url):
	kod = getPage(url)
	cena = kod.find('\\\'price\\\'')
	kwota = kod[cena+13:cena+30]
	kwota = kwota[:kwota.find('\'')-1]
	return kwota

def fryzjer(url):
	kod = getPageClassAll(url,'salonPrices')
	men = kod[1]
	ceny = men.findChildren(class_='salonPriceValue', recursive=True)
	return ceny[0].get_text()

def prad(url):
	kod = getPage(url)
	cena = kod.find('background:yellow;mso-highlight:yellow')
	kwota = kod[cena+41:cena+100]
	kwota = kwota[:kwota.find('-')]
	return kwota

def auchan(url):
	page = requests.get(url)
	kod = BeautifulSoup(page.content, 'html.parser')
	try:
		kod = kod.get_text()
		cena = kod.find('product_unitprice_ati')
		kwota = kod[cena+23:cena+50]
		kwota = kwota[:kwota.find(',')]
		return kwota
	except:
		print("problem z: ", url)
		return '0'

def m2(url):
	kwota = getPageId(url,'locationPageLink').get_text()
	kwota = kwota[kwota.find('(')+1:kwota.find('zł/m')]
	return kwota

def karma(url):
	return getPageClass(url,'main-price color').get_text()

def aspiryna(url):
	return getPageClass(url,'product-card-product-price').get_text()

def rolex(url):
	return getPageClass(url,'price dig').get_text()

def benzyna(url):
	return getPageClass(url,'price').get_text()

def kasjer(url):
	return getPageClass(url,'js-median-gross').get_text()

def lot(url):
	return getPageClass(url,' length-5').get_text()

def upc(url):
	kwota = getPageClass(url,'lgi-hdr-9 ph2-d l-h6 m-h7 lgi-txtsd-default').get_text()
	kwota = kwota[:kwota.find('zł/mies')]
	return kwota

def telefon(url):
	kod = getPage(url)
	cena = kod.find('js-range_min js-filters_priceMin')
	kwota = kod[cena+55:cena+100]
	kwota = kwota[:kwota.find('>')-1]
	return kwota

def lekarz(url):
	lek = getPageClassAll(url,'text-muted offset-0')
	kwota = []
	for x in lek:
		kwota.append(f.zrobCene(x.get_text()))
	return [statistics.mean(kwota),statistics.median(kwota)]

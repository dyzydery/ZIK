# coding=utf-8
#! python3
import urllib.request
import requests
import datetime
import koszyk
import funkcyjki as f
from kindle import getMinCenaKindla
import re
from bs4 import BeautifulSoup
from skrobaczka import getPage,printPage,getPageId,getPageClass,getPageClassAll
import statistics
print('Złoty Indeks Kieleckiego')
print(datetime.datetime.now())


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


def skanujKoszyk():
	l = len(koszyk.koszyk)+1
	i = 0
	for x in koszyk.koszyk:
		print ('[==',int(i/l*100),'% ',f.CYELLOW2 + x[0] + f.CEND,' ==]',end="               \r")
		if (x[2].find('tesco')!=-1):
			cart[x[0]] = f.zrobCene(tesco(x[0],x[2]))
		elif (x[0]=='buty'):
			cart[x[0]] = f.zrobCene(kazar(x[2]))
		elif (x[0]=='whisky' or x[0]=='piwo'):
			cart[x[0]] = f.zrobCene(auchan(x[2]))
		elif (x[0]=='karma'):
			cart[x[0]] = f.zrobCene(karma(x[2]))
		elif (x[0]=='aspiryna'):
			cart[x[0]] = f.zrobCene(aspiryna(x[2]))
		elif (x[0]=='rolex'):
			cart[x[0]] = f.zrobCene(rolex(x[2]))
		elif (x[0]=='benzyna'):
			cart[x[0]] = f.zrobCene(benzyna(x[2]))
		elif (x[0]=='prad'):
			cart[x[0]] = f.zrobCene(prad(x[2]))
		elif (x[0]=='upc'):
			cart[x[0]] = f.zrobCene(upc(x[2]))
		elif (x[0]=='m2wtorny'):
			cart[x[0]] = f.zrobCene(m2(x[2]))
		elif (x[0]=='m2pierwotny'):
			cart[x[0]] = f.zrobCene(m2(x[2]))
		elif (x[0]=='telefon'):
			cart[x[0]] = f.zrobCene(telefon(x[2]))
		elif (x[0]=='kasjer'):
			cart[x[0]] = f.zrobCene(kasjer(x[2]))
		elif (x[0]=='fryzjer'):
			cart[x[0]] = f.zrobCene(fryzjer(x[2]))
		elif (x[0]=='lot'):
			cart[x[0]] = f.zrobCene(lot(x[2]))
		elif (x[0]=='lekarz'):
			z=lekarz(x[2])
			cart[x[0]+'_Mean'] = z[0]
			cart[x[0]+'_Median'] = z[1]
		i+=1
	print ('[==',int(i/l*100),'% ',f.CYELLOW2 + 'kindle' + f.CEND,' ==]',end ="               \r")
	cart['kindle'] = getMinCenaKindla()
	i+=1

def printKoszyk():
	i = 0
	for e,v in cart.items():
		if i%2==0:
			print(f.CGREYBG+'{:15}'.format(e)+f.CEND,': ',f.CGREEN2+str(v)+f.CEND)
		else:
			print('{:15}'.format(e),': ',f.CGREEN2+str(v)+f.CEND)
		i+=1


a = koszyk.koszyk[20]
# printPage(a[2])
# print('Cena', fryzjer(a[2]))

cart = {'TimeStamp':str(datetime.datetime.now().replace(microsecond=0))}
skanujKoszyk()
printKoszyk()
f.saveCSV(cart)

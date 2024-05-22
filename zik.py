# coding=utf-8
#! python3
import urllib.request
import requests
import datetime
import koszyk
import funkcyjki as f
# from kindle import getMinCenaKindla
import re
from bs4 import BeautifulSoup
from skrobaczka import *
import statistics
from baza import DBinsert
from plot import wykresuj
from inflacja import calculateInflation
print('Złoty Indeks Kieleckiego')
print(datetime.datetime.now())
cart = {'TimeStamp':str(datetime.datetime.now().replace(microsecond=0))}
def skanujKoszyk():
    l = len(koszyk.koszyk)+1
    i = 0
    for x in koszyk.koszyk:
        print ('[==',int(i/l*100),'% ',f.CYELLOW2 + x[0] + f.CEND,' ==]',end="               \r")
        if (x[2].find('frisco')!=-1):
            cart[x[0]] = f.zrobCene(frisco(x[2]))
        elif (x[0]=='buty'):
            cart[x[0]] = f.zrobCene(kazar(x[2]))
        elif (x[0]=='whisky'):
            cart[x[0]] = f.zrobCene(alkohol(x[2]))
        # elif (x[0]=='piwo'):
        #     cart[x[0]] = f.zrobCene(piwo(x[2]))
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
        elif (x[0]=='bigmac'):
            cart[x[0]] = f.zrobCene(bigmac(x[2]))
        elif (x[0]=='lot'):
            #na razie nie ma lotow, markujemy zeby nie bylo syfu w bazie
            cart[x[0]] = -1.0
        elif (x[0]=='kindle'):
            cart[x[0]] = f.zrobCene(kindl(x[2]))
        elif (x[0]=='lekarz'):
            z=lekarz(x[2])
            cart[x[0]+'_Mean'] = z[0]
            cart[x[0]+'_Median'] = z[1]
        elif (x[0]=='auto'):
            z=otomoto(x[2])
            cart[x[0]+'_Mean'] = z[0]
            cart[x[0]+'_Median'] = z[1]
        i+=1
    print ('[==',int(i/l*100),'% ',f.CYELLOW2 + 'waluty' + f.CEND,' ==]',end ="               \r")
    currency = waluty()
    cart['xau'] = currency['xau']
    cart['usd'] = currency['usd']
    cart['chf'] = currency['chf']

def WyliczZIK():
    skanujKoszyk()
    inf = calculateInflation()
    # f.printKoszyk(cart)
    f.printKoszykInflacja(cart,inf)
    DBinsert(cart)
    f.saveCSV(cart)
    wykresuj()


url=koszyk.getURL('auto')
# url='https://ismartfony.pl/samsung-galaxy-s24-ultra-5g-12-512-gb-czarny'
# printPage(url)
# print((otomoto(url)))
WyliczZIK()

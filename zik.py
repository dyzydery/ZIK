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
from skrobaczka import *
import statistics
print('Złoty Indeks Kieleckiego')
print(datetime.datetime.now())




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
        elif (x[0]=='auto'):
            z=otomoto(x[2])
            cart[x[0]+'_Mean'] = z[0]
            cart[x[0]+'_Median'] = z[1]
        i+=1
    print ('[==',int(i/l*100),'% ',f.CYELLOW2 + 'kindle' + f.CEND,' ==]',end ="               \r")
    cart['kindle'] = getMinCenaKindla()
    i+=1
    print ('[==',int(i/l*100),'% ',f.CYELLOW2 + 'waluty' + f.CEND,' ==]',end ="               \r")
    currency = waluty()
    cart['xau'] = currency['xau']
    cart['usd'] = currency['usd']
    cart['chf'] = currency['chf']

def printKoszyk():
    i = 0
    for e,v in cart.items():
        if i%2==0:
            print(f.CGREYBG+'{:15}'.format(e)+f.CEND,': ',f.CGREEN2+str(v)+f.CEND)
        else:
            print('{:15}'.format(e),': ',f.CGREEN2+str(v)+f.CEND)
        i+=1


a = koszyk.koszyk[15]
print(getPage(a[2]))
printPage(a[2])
# print('Cena srednia', otomoto(a[2])[0])

cart = {'TimeStamp':str(datetime.datetime.now().replace(microsecond=0))}
# skanujKoszyk()
# printKoszyk()
# f.saveCSV(cart)

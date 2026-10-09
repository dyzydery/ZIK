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
from time import sleep
#from plot import wykresuj
# from inflacja import calculateInflation
print('Złoty Indeks Kieleckiego')
print(datetime.datetime.now())
cart = {'TimeStamp':str(datetime.datetime.now().replace(microsecond=0))}

SCRAPERY = {
    'buty':    kazar,
    'whisky':  alkohol,
    'upc':     upc,
    'm2wtorny':    m2,
    'm2pierwotny': m2,
    'karma':    karma,
    'aspiryna':  aspiryna,
    'rolex':     rolex,
    'benzyna':    benzyna,
    'prad': prad,
    'telefon':  telefon,
    'kasjer':     kasjer,
    'fryzjer':    fryzjer,
    'bigmac': bigmac,
    'lot':    lot,
    'kindle':  kindl,
}
WALUTY = {'xau','usd','chf'}
PODWOJNE = {'lekarz': lekarz,'auto': otomoto}
def pobierz(towar, funkcja, url, blad=-1.0):
    try:
        return funkcja(url)
    except Exception as e:
        print(f'BLAD {towar}: {type(e).__name__}: {e}')
        return blad

def skanujKoszyk():
    for nazwa, opis, url in koszyk.koszyk:
        if nazwa in WALUTY:
            continue
        if 'frisco' in url:
            cart[nazwa] = pobierz(nazwa,frisco,url)
            if cart[nazwa] == -1:
                print(f'Ponawiam próbę {nazwa}')
                sleep(3)
                cart[nazwa] = pobierz(nazwa,frisco,url)
        elif nazwa in PODWOJNE:
            z=pobierz(nazwa,PODWOJNE[nazwa],url,[-1.0,-1.0])
            cart[nazwa+'_Mean'] = z[0]
            cart[nazwa+'_Median'] = z[1]
        else:
            cart[nazwa] = pobierz(nazwa, SCRAPERY[nazwa], url)
    currency = waluty()
    cart['xau'] = currency['xau']
    cart['usd'] = currency['usd']
    cart['chf'] = currency['chf']

def WyliczZIK():
    skanujKoszyk()
    # inf = calculateInflation()
    # f.printKoszyk(cart)
    # f.printKoszykInflacja(cart,inf)
    DBinsert(cart)
    f.saveCSV(cart)
    # wykresuj()

if __name__ == '__main__':
    WyliczZIK()


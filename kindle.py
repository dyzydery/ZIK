# coding=utf-8
#! python3
from skrobaczka import getPage,printPage,getPageId,getPageClass
from funkcyjki import zrobCene
import statistics
kindl = [
['euro','https://www.euro.com.pl/czytniki-ebookow/amazon-czytnik-kindle-pw-4-8gb-black-bez-reklam.bhtml?from=ceneo&p=699.00&cr=0&t=20200430-1443'],
['media','https://www.mediaexpert.pl/komputery-i-tablety/tablety-i-e-booki/czytniki-e-bookow/czytnik-kindle-paperwhite-4-czarny-b07741s7y8-ekran-dotykowy-6-cali-rozdzielczosc-1448x1072-8gb-doswietlana-matryca-e-ink-wodood?utm_source=Ceneo&utm_medium=cpc&utm_content=894887&utm_campaign=2020-04&ceneo_spo=false'],
['bit','https://bitcomputer.pl/pl/p/KINDLE-PAPERWHITE-4-8GB-BEZ-REKLAM-B07741S7Y8/56606?Bit%20Computer'],
['xkom','https://www.x-kom.pl/p/465445-czytnik-ebook-amazon-kindle-paperwhite-4-8gb-ipx8-bez-reklam-czarny.html?utm_source=ceneo&utm_medium=comparison&utm_campaign=ceneo_click']]

def skanujKindle():
    for x in kindl:
        if x[0]=='media':
            x.append(zrobCene(getPageClass(x[1],'a-price_price').get_text()))
        elif x[0]=='euro':
            x.append(zrobCene(getPageClass(x[1],'price-normal selenium-price-normal').get_text()))
        elif x[0]=='bit':
            x.append(zrobCene(getPageClass(x[1],'main-price').get_text()))
        elif x[0]=='xkom':
            x.append(zrobCene(getPageClass(x[1],'u7xnnm-4 iVazGO').get_text()))

def statystyka():
    a = [x[2] for x in kindl]
    print('Srednia: ',statistics.mean(a))
    print('Mediana: ',statistics.median(a))
    print('Minimum: ',min(a))

def getMin():
    return min([x[2] for x in kindl])

def printKindle():
    for x in kindl:
        print (x[0],': ',x[2])

def getMinCenaKindla():
    skanujKindle()
    return getMin()

def pokazKindle():
    skanujKindle()
    printKindle()
    statystyka()

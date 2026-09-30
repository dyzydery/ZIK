# coding=utf-8
#! python3
import csv
from datetime import datetime

def isGood(cena):
    try:
        cena = float(cena)
    except:
        return False
    if cena <=0:
        return False
    else:
        return True

def deltaTime(t):
    date1 = datetime.strptime(ostatni['TimeStamp'], "%Y-%m-%d %H:%M:%S")
    date2 = datetime.strptime(t, "%Y-%m-%d %H:%M:%S")
    difference = (date1.date() - date2.date()).days
    return str(difference)

print('Sprawdzanie stanu zdrowia danych')
with open("zikDB.csv", "r") as f:
    czytnik = csv.DictReader(f)
    wiersze = list(czytnik)
    naglowki = czytnik.fieldnames
ostatni = wiersze[-1]
poprzedni = wiersze[-2]
bledne=[]
regresja=[]
martwe=[]
for rzecz in naglowki:
    if rzecz == "TimeStamp" or rzecz == "xau" or rzecz == "usd" or rzecz == "chf":
        continue
    if not isGood(ostatni[rzecz]):
        bledne.append(rzecz)
for x in bledne:
    if isGood(poprzedni[x]):
        regresja.append(x)
print(f'REGRESJA: {regresja}')
for b in bledne:
    for w in reversed(wiersze[:-1]):
        if isGood(w[b]):
            martwe.append(b+": "+deltaTime(w['TimeStamp'])+'d')
            break
print(f'Martwe {martwe}')


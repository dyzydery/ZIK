# coding=utf-8
#! python3
import re
import csv
import koszyk
def zrobCene(x):
    x = x.replace(',','.')
    return float(re.sub('[^0-9.]', '', x))

def saveCSV(cart):
    fieldnames = [row[0] for row in koszyk.koszyk]
    i = fieldnames.index('lekarz')
    fieldnames[i]='lekarz_Mean'
    fieldnames.insert(i+1,'lekarz_Median')
    fieldnames.append('kindle')
    fieldnames.insert(0,'TimeStamp')
    with open('zikDB.csv', 'a') as csvfile:
        print('Saved in CSV')
        csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csvwriter.writerow(cart)

def znajdzSrednia(x):
    cos=0
    for a in x:
        cos=cos+a
    dlugosc=len(x)
    srednia=(cos/dlugosc)
    return srednia





CEND      = '\33[0m'
CGREY    = '\33[90m'
CRED2    = '\33[91m'
CGREEN2  = '\33[92m'
CYELLOW2 = '\33[93m'
CBLUE2   = '\33[94m'
CVIOLET2 = '\33[95m'
CBEIGE2  = '\33[96m'
CWHITE2  = '\33[97m'

CGREYBG    = '\33[100m'
CREDBG2    = '\33[101m'
CGREENBG2  = '\33[102m'
CYELLOWBG2 = '\33[103m'
CBLUEBG2   = '\33[104m'
CVIOLETBG2 = '\33[105m'
CBEIGEBG2  = '\33[106m'
CWHITEBG2  = '\33[107m'

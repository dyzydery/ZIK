# coding=utf-8
#! python3
from baza import *
from datetime import datetime
from funkcyjki import printKoszyk

def get365timestamp(teraz):
    timestamps = DBgetTimestamps()
    y2yID = teraz
    for x in timestamps:
        a = datetime.strptime (x[0],'%Y-%m-%d %H:%M:%S')
        diff = (teraz-a).days
        if diff>365:
            y2yID = a
    return str(y2yID)

def calculateInflation():
    row = DBgetRowByTimestamp(get365timestamp(datetime.now()))[0]
    teraz = DBgetLastRow()[0]
    inflacja = [0]*len(row)
    try:
        names = ['id','timestamp','kielecki','pizza','maslo','jablka','makaron','chleb','mydlo','kurczak','jajka','rolex','whisky','piwo','buty','auto_Mean','auto_Median','telefon','bigmac','m2wtorny','m2pierwotny','benzyna','lot','fryzjer','upc','prad','lekarz_Mean','lekarz_Median','aspiryna','karma','kasjer','kindle','xau','chf','usd']
        for i in range (2,len(row)):
            stare = float(row[i])
            nowe = float(teraz[i])
            if stare > 0:
                inflacja[i] = (nowe-stare)/nowe*100
            # print(names[i],": ",stare," | ",nowe, " inflacja: ", inflacja[i],"%")
    except Exception as e:
        print(e)
    # print(inflacja)
    return inflacja


# calculateInflation(123)

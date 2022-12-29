# coding=utf-8
#! python3
from baza import *
from datetime import datetime
from funkcyjki import printKoszyk
import statistics

def get365timestamp(teraz):
    timestamps = DBgetTimestamps()
    y2yID = teraz
    for x in timestamps:
        a = datetime.strptime (x[0],'%Y-%m-%d %H:%M:%S')
        diff = (teraz-a).days
        if diff>365:
            y2yID = a
    print (str(y2yID))
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
            if stare < 0:
                stare = DBgetNotNullValue(row[0],names[i])
                # print(propsy)
                #Stopa inflacji  = [(poziom cen w roku t – poziom cen w roku t-1) / poziom cen w roku t-1] * 100%
            inflacja[i] = (nowe-stare)/stare*100
            # print(names[i],": ",stare," | ",nowe, " inflacja: ", inflacja[i],"%")
                # food
                #     'kielecki','pizza','maslo','jablka','makaron','chleb','mydlo','kurczak','jajka','piwo','bigmac'
                # commodities
                #     'auto_Mean','auto_Median','m2wtorny','m2pierwotny','benzyna','upc','prad','lekarz_Mean','lekarz_Median','aspiryna','karma'
                # luxuries
                #     'rolex','whisky','buty','telefon','lot','kindle','fryzjer'
                # basics
                #       'kielecki','pizza','maslo','jablka','makaron','chleb','mydlo','kurczak','jajka','piwo','bigmac','aspiryna','karma'
    except Exception as e:
        print(e)
    print ("FOOD Inflantion: ",foodInflation(inflacja))
    print ("Commodities Inflantion: ",commoditiesInflation(inflacja))
    print ("Luxury Inflantion: ",luxuryInflation(inflacja))
    # print(inflacja)
    return inflacja

def luxuryInflation(inf):
    # luxuries
    #     'rolex','whisky','buty','telefon','lot','kindle','fryzjer'
    lux = inf[11:13]
    lux.append(inf[14])
    lux.append(inf[17])
    lux.append(inf[23])
    lux.append(inf[31])
    return statistics.mean(lux)

def commoditiesInflation(inf):
    # commodities
    #     'auto_Mean','auto_Median','m2wtorny','m2pierwotny','benzyna','upc','prad','lekarz_Mean','lekarz_Median',
    com = inf[15:17]+inf[19:22]+inf[24:28]
    return statistics.mean(com)

def foodInflation(inf):
    # food
    #     'kielecki','pizza','maslo','jablka','makaron','chleb','mydlo','kurczak','jajka','piwo','bigmac'
    food = inf[2:11]
    food.append(inf[13])
    food.append(inf[18])
    return statistics.mean(food)

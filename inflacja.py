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

def calculateInflation(cart):
    row = DBgetRowByTimestamp(get365timestamp(datetime.now()))
    cartOld = []
    names = ['timestamp','kielecki','pizza','maslo','jablka','makaron','chleb','mydlo','kurczak','jajka','rolex','whisky','piwo','buty','auto_Mean','auto_Median','telefon','bigmac','m2wtorny','m2pierwotny','benzyna','lot','fryzjer','upc','prad','lekarz_Mean','lekarz_Median','aspiryna','karma','kasjer','kindle','xau','chf','usd']
    # for x in row:
    #     cart
    # printKoszyk(row)



# calculateInflation(123)

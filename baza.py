# coding=utf-8
#! python3
import sqlite3
from sqlite3 import Error
import csv

def sql_connection():
    try:
        con = sqlite3.connect('zik.db')
        return con
    except Error:
        print(Error)

def sql_insert(con, entities, table):
    cursorObj = con.cursor()
    cursorObj.execute('INSERT INTO '+table+'(timestamp,kielecki,pizza,maslo,jablka,makaron,chleb,mydlo,kurczak,jajka,rolex,whisky,piwo,buty,auto_Mean,auto_Median,telefon,bigmac,m2wtorny,m2pierwotny,benzyna,lot,fryzjer,upc,prad,lekarz_Mean,lekarz_Median,aspiryna,karma,kasjer,kindle,xau,chf,usd) VALUES(?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?,?, ?, ?, ?,?)', entities)
    con.commit()

def DBinsert(row):
    con = sql_connection()
    cenaEnt = (row['TimeStamp'],row['kielecki'],row['pizza'],row['maslo'],row['jablka'],row['makaron'],row['chleb'],row['mydlo'],row['kurczak'],row['jajka'],row['rolex'],row['whisky'],row['piwo'],row['buty'],row['auto_Mean'],row['auto_Median'],row['telefon'],row['bigmac'],row['m2wtorny'],row['m2pierwotny'],row['benzyna'],row['lot'],row['fryzjer'],row['upc'],row['prad'],row['lekarz_Mean'],row['lekarz_Median'],row['aspiryna'],row['karma'],row['kasjer'],row['kindle'],row['xau'],row['chf'],row['usd'])
    sql_insert(con, cenaEnt,'ceny')
    x = row['xau']
    zikEnt = (row['TimeStamp'],row['kielecki']/x,row['pizza']/x,row['maslo']/x,row['jablka']/x,row['makaron']/x,row['chleb']/x,row['mydlo']/x,row['kurczak']/x,row['jajka']/x,row['rolex']/x,row['whisky']/x,row['piwo']/x,row['buty']/x,row['auto_Mean']/x,row['auto_Median']/x,row['telefon']/x,row['bigmac']/x,row['m2wtorny']/x,row['m2pierwotny']/x,row['benzyna']/x,row['lot']/x,row['fryzjer']/x,row['upc']/x,row['prad']/x,row['lekarz_Mean']/x,row['lekarz_Median']/x,row['aspiryna']/x,row['karma']/x,row['kasjer']/x,row['kindle']/x,row['xau']/x,row['chf']/x,row['usd']/x)
    sql_insert(con, zikEnt,'zik')
    print ('Inserting row in DB')

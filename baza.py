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

def sql_insert(con, entities):
    cursorObj = con.cursor()
    cursorObj.execute('INSERT INTO ceny(timestamp,kielecki,pizza,maslo,jablka,makaron,chleb,mydlo,kurczak,jajka,rolex,whisky,piwo,buty,auto_Mean,auto_Median,telefon,bigmac,m2wtorny,m2pierwotny,benzyna,lot,fryzjer,upc,prad,lekarz_Mean,lekarz_Median,aspiryna,karma,kasjer,kindle,xau,chf,usd) VALUES(?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?,?, ?, ?, ?,?)', entities)
    con.commit()

def DBinsert(row):
    con = sql_connection()
    entities = (row['TimeStamp'],row['kielecki'],row['pizza'],row['maslo'],row['jablka'],row['makaron'],row['chleb'],row['mydlo'],row['kurczak'],row['jajka'],row['rolex'],row['whisky'],row['piwo'],row['buty'],row['auto_Mean'],row['auto_Median'],row['telefon'],row['bigmac'],row['m2wtorny'],row['m2pierwotny'],row['benzyna'],row['lot'],row['fryzjer'],row['upc'],row['prad'],row['lekarz_Mean'],row['lekarz_Median'],row['aspiryna'],row['karma'],row['kasjer'],row['kindle'],row['xau'],row['chf'],row['usd'])
    sql_insert(con, entities)
    print ('Inserting row in DB')

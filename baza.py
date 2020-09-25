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
    cursorObj.execute('INSERT INTO ceny(timestamp,kielecki,pizza,maslo,jablka,makaron,chleb,mydlo,kurczak,jajka,rolex,whisky,piwo,buty,auto_Mean,auto_Median,telefon,bigmac,m2wtorny,m2pierwotny,benzyna,lot,fryzjer,upc,prad,lekarz_Mean,lekarz_Median,aspiryna,karma,kasjer,xau,chf,usd,kindle) VALUES(?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?,?, ?, ?, ?,?)', entities)
    con.commit()

def DBinsert(cart):
    row = cart.values()
    print(row)
    # con = sql_connection()
    # entities = (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14],row[15],row[16],row[17],row[18],row[19],row[20],row[21],row[22],row[23],row[24],row[25],row[26],row[27],row[28],row[29],row[30],row[31],row[32],row[33])
    # sql_insert(con, entities)
    # print ('Inserting row in DB')

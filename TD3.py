
import requests
import json
import sqlite3
import datetime 
from datetime import datetime, timedelta



def Display_Currencies():
    currencies = requests.get("https://api.pro.coinbase.com/products")
    y = currencies.json()
    list_cur= []    

    for i in y:
        mybool = False
        for a in list_cur:
            if i['base_currency'] == a:
                mybool = True
        if mybool == False:
            list_cur.append(i['base_currency'])
    print(list_cur)



def getDepth(direction ,pair ):
    currencies = requests.get("https://api.pro.coinbase.com/products/"+ pair + "/ticker")
    y = currencies.json()


    print(direction+": " +y[direction])

def OrderBook(pair):
    currencies = requests.get("https://api.pro.coinbase.com/products/"+ pair + "/book?level=2")
    y = currencies.json()
    print("Bids:")
    print(y['bids'])
    print("Asks:")
    print(y['asks'])

def candles(pair, duration):
    currencies = requests.get("https://api.pro.coinbase.com/products/" + pair + "/candles?start=2020-01-01T00%3A00%3A00.0Z"+ "&granularity="+ duration)
    y = currencies.json()

    setTableName = str("candles")
    tableCreationStatement = "CREATE TABLE " + setTableName + "(date INT,low REAL, high REAL, open REAL, close REAL, volume REAL)"
    conn =sqlite3.connect('candles.db')
    c = conn.cursor()
    c.execute(tableCreationStatement)


    for a in y:
        c.execute("insert into "+setTableName+" values (?,?,?,?,?,?)",[a[0],a[1],a[2],a[3],a[4],a[5]])
        conn.commit()
    conn.close
    for row in c.execute("SELECT * FROM candles"):
        print(row)
    
def refreshData(pair):
    currencies = requests.get("https://api.pro.coinbase.com/products/" + pair + "/trades")
    y = currencies.json()

    setTableName = str("trade")
    tableCreationStatement = "CREATE TABLE " + setTableName + "(Id INTEGER PRIMARY KEY, time TEXT, price REAL, size REAL, side TEXT)"
    conn =sqlite3.connect('trades.db')
    c = conn.cursor()
    c.execute(tableCreationStatement)

    for a in y:
        c.execute("insert into "+setTableName+" values (?,?,?,?,?)",[a['trade_id'],a['time'],a['price'],a['size'],a['side']])
        conn.commit()
    conn.close
    for row in c.execute("SELECT * FROM trade"):
        print(row)

def createOrder(direction, price, amount, pair, orderType):
    payload = {'side': direction, 'price':price , 'size':amount,'product_id' : pair}
    currencies = requests.post("https://api.pro.coinbase.com/orders",params = payload)
    y = currencies.json()
    print(y)








i= 2
while i!=0:
    print("Que voulez vous faire?")
    print("Taper 1 pour Afficher toutes les cryptomonnaies disponibles")
    print("Taper 2 pour Afficher le 'bid' ou le 'ask' d'un asset")
    print("Taper 3 pour Afficher l'order book d'un asset")
    print("Taper 4 pour Afficher les 'candles' d'un asset")
    print("Taper 5 pour Afficher les derniers trades d'un asset")

    print("Taper 0 pour quiter")
    i = int(input())

    if i ==1:
        Display_Currencies()

    if i == 2:
        a=3
        while a>=2:
            print("Que voulez vous Afficher?")
            print("Taper 0 pour Afficher le bid")
            print("Taper 1 pour Afficher le ask")
            a= int(input())
        if a == 0:
            direction = 'bid'
        else:
            direction = 'ask'
        print("Entrez le nom de la pair (ex: BTC-USD):")
        pair = input()
        getDepth(direction,pair)

    if i==3:
        print("Entrez le nom de la pair (ex: BTC-USD):")
        pair = input()
        OrderBook(pair)

    if i ==4:
        print("Entrez le nom de la pair (ex: BTC-USD):")
        pair = input()
        print("Entrez la durée des candles en seconde")
        duree = input()
        candles(pair,duree)

    if i==5:
        print("Entrez le nom de la pair (ex: BTC-USD):")
        pair = input()
        refreshData(pair)
       




        


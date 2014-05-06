# get_prices.py

import time
import random
import datetime
import sqlite3

def time_stamp2date_time(ts):
    pattern = '%Y-%m-%d %H:%M:%S'
    es = int(time.mktime(time.strptime(ts, pattern)))
    dt = datetime.datetime.utcfromtimestamp(es)  # for UTC
    return dt

def get_max_date():
    db = sqlite3.connect("shares.db")
    max_date =  db.execute(''' select max (Timestamp) from price''').fetchall()[0][0]
    db.close()
    return max_date

def get_current_prices(current_date): 
    db = sqlite3.connect("shares.db")
    sql = ''' select symbol, price from price where Timestamp = "%s" ''' % current_date 
    current_prices  =  db.execute(sql ).fetchall()
    db.close()

    prices={}
    for current_price in current_prices:
        symbol = current_price[0]
        value = current_price[1]
        prices[symbol] = value

    return prices

def get_new_prices(current_prices): 
    new_prices = {} 
    for name , value in current_prices.items():
        r = random.uniform(-1,1)
        change = int(value * r/4)
        value += change
        new_prices[name] = value
         
    return new_prices

def insert_prices(date, prices):
    
    db = sqlite3.connect("shares.db")
    for symbol, price in prices.items():
        print 'INSERT %s, %s, %s' %(date,symbol,price)
        sql = "INSERT INTO price(Timestamp,symbol,price) VALUES ('%s','%s',%s)" %(date,symbol,price)
        db.execute(sql )
    db.commit() 
    db.close()

def insert_new_price():
    max_date = time_stamp2date_time(get_max_date()) 

    current_prices = get_current_prices(max_date)
    new_prices = get_new_prices(current_prices)


    new_date =  max_date + datetime.timedelta(days=1)
    insert_prices(new_date,new_prices)


def insert_new_prices():
    while True:
        insert_new_price()
        time.sleep(10)


insert_new_prices()




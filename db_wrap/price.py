# price.py

import sqlite3

def create(c):
    c.execute('''CREATE TABLE price
             (Id integer PRIMARY KEY,
              Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
              symbol text, price real )''')


def insert_start_data(c):
    c.execute("INSERT INTO price(Timestamp,symbol,price) VALUES ('2000-01-01 12:00:00','AA',90)")
    c.execute("INSERT INTO price(Timestamp,symbol,price) VALUES ('2000-01-01 12:00:00','BB',45)")
    c.execute("INSERT INTO price(Timestamp,symbol,price) VALUES ('2000-01-02 12:00:00','AA',93)")
    c.execute("INSERT INTO price(Timestamp,symbol,price) VALUES ('2000-01-02 12:00:00','BB',42)")
    c.execute("INSERT INTO price(Timestamp,symbol,price) VALUES ('2000-01-03 12:00:00','AA',93)")
    c.execute("INSERT INTO price(Timestamp,symbol,price) VALUES ('2000-01-03 12:00:00','BB',49)")
    c.execute("INSERT INTO price(Timestamp,symbol,price) VALUES ('2000-01-04 12:00:00','AA',97)")
    c.execute("INSERT INTO price(Timestamp,symbol,price) VALUES ('2000-01-04 12:00:00','BB',47)")
    c.execute("INSERT INTO price(Timestamp,symbol,price) VALUES ('2000-01-05 12:00:00','AA',90)")
    c.execute("INSERT INTO price(Timestamp,symbol,price) VALUES ('2000-01-05 12:00:00','BB',50)")
    #c.execute("INSERT INTO price(Timestamp,symbol,price) VALUES ('2000-01-05 18:00:00','AA',91)")
    c.execute("INSERT INTO price(Timestamp,symbol,price) VALUES ('2000-01-06 12:00:00','AA',85)")
    c.execute("INSERT INTO price(Timestamp,symbol,price) VALUES ('2000-01-06 12:00:00','BB',35)")
    c.execute("INSERT INTO price(Timestamp,symbol,price) VALUES ('2000-01-07 12:00:00','AA',95)")
    c.execute("INSERT INTO price(Timestamp,symbol,price) VALUES ('2000-01-07 12:00:00','BB',50)")

def get_prices(db):
    return db.execute("SELECT Id, Timestamp, symbol,price from price").fetchall()


def get_max_date(db):
    max_date =  db.execute(''' select max (Timestamp) from price''').fetchall()[0][0]
    return max_date

def get_share_price(db,tmp_date, symbol):
    sql = " select price from price where Timestamp = '%s' and symbol = '%s' " %(tmp_date, symbol)
    price =  db.execute(sql).fetchall()[0][0]
    return price 


def get_share_prices(db, tmp_date):
    sql = " select symbol, price from price where Timestamp = '%s' " %(tmp_date)
    prices =  db.execute(sql).fetchall()
    return prices





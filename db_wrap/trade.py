# trade.py

def create(c):
       print 'Creating table: trade'
       c.execute('''CREATE TABLE trade
             (Id integer PRIMARY KEY,
              Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
              symbol int ,
              quantity int,
              price real )''')

def insert(db,tmp_date,symbol,quantity,price):
    sql = "INSERT INTO trade(Timestamp,symbol,quantity,price) VALUES ('%s','%s',%s,%s)"  %(tmp_date,symbol,quantity,price)
    print sql
    db.execute(sql)
    db.commit()
    pass


def insert_start_data(c):
    pass
    c.execute("INSERT INTO trade(Timestamp,symbol,quantity,price) VALUES ('2000-02-02 12:00:00','AA',0,90)")
    c.execute("INSERT INTO trade(Timestamp,symbol,quantity,price) VALUES ('2000-02-02 12:00:00','BB',0,40)")
    #c.execute("INSERT INTO trade(Timestamp,symbol,quantity,price) VALUES ('2000-02-03 12:00:00','BB',20,90)")
    #c.execute("INSERT INTO trade(Timestamp,symbol,quantity,price) VALUES ('2000-02-04 12:00:00','AA',-10,95)")
    #c.execute("INSERT INTO shares(date,trans,symbol,qty,price) VALUES ('2006-01-05','BUY','AA',100,35.14)")
    #c.execute("INSERT INTO shares(date,trans,symbol,qty,price) VALUES ('2006-01-06','BUY','BB',-50,5.40)")

def get_trades(db):
    return db.execute("SELECT Id, Timestamp, symbol,quantity,price from trade").fetchall()

def get_trades_inventory(db):
    return db.execute("SELECT symbol, sum(quantity) from trade group by symbol ").fetchall()




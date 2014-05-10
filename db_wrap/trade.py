# trade.py

def create(c):
       print 'Creating table: trade'
       c.execute('''CREATE TABLE trade
             (Id integer PRIMARY KEY,
              Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
              symbol int ,
              quantity int,
              price real )''')

def insert_start_data(c):
    c.execute("INSERT INTO trade(Timestamp,symbol,quantity,price) VALUES ('2000-02-02 12:00:00','AA',10,90)")
    c.execute("INSERT INTO trade(Timestamp,symbol,quantity,price) VALUES ('2000-02-03 12:00:00','AA',20,90)")
    c.execute("INSERT INTO trade(Timestamp,symbol,quantity,price) VALUES ('2000-02-04 12:00:00','AA',-10,95)")
    c.execute("INSERT INTO shares(date,trans,symbol,qty,price) VALUES ('2006-01-05','BUY','AA',100,35.14)")
    c.execute("INSERT INTO shares(date,trans,symbol,qty,price) VALUES ('2006-01-06','BUY','BB',-50,5.40)")

def get_trades(db):
    return db.execute("SELECT Id, Timestamp, symbol,quantity,price from trade").fetchall()


# share.py

def create(c):
    c.execute('''CREATE TABLE share
             (Id integer PRIMARY KEY,
              Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
              symbol text )''')

def insert_start_data(c):
    c.execute("INSERT INTO share(symbol) VALUES ('AA')")
    c.execute("INSERT INTO share(symbol) VALUES ('BB')")

def get_shares(db):
    return db.execute("SELECT Id, Timestamp, symbol from share").fetchall()


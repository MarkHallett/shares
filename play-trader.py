# play-trader.py

import os
import json
import sqlite3
from flask import Flask, render_template
from flask import request, redirect
from flask import g


app = Flask(__name__)

def initialise_db():
  
    print 'initialise_db!!'
    if os.path.isfile('shares.db'):
       print 'shares.db exists'
       return

    print 'shares.db does not exists'
    db = sqlite3.connect("shares.db")

    c = db.cursor()

    # Create tables
    c.execute('''CREATE TABLE share
             (Id integer PRIMARY KEY,
              Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
              symbol text )''')

    c.execute('''CREATE TABLE price
             (Id integer PRIMARY KEY, 
              Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
              symbol text, price real )''')

    c.execute('''CREATE TABLE trade
             (Id integer PRIMARY KEY, 
              Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
              symbol int , 
              quantity int, 
              price real )''')


    c.execute('''CREATE TABLE shares
             (Id integer PRIMARY KEY, date text, trans text, symbol text, qty real, price real)''')

    # Insert a row of data
    c.execute("INSERT INTO share(symbol) VALUES ('AA')")
    c.execute("INSERT INTO share(symbol) VALUES ('BB')")
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
    c.execute("INSERT INTO price(Timestamp,symbol,price) VALUES ('2000-01-05 18:00:00','AA',91)")
    c.execute("INSERT INTO price(Timestamp,symbol,price) VALUES ('2000-01-06 12:00:00','AA',85)")
    c.execute("INSERT INTO price(Timestamp,symbol,price) VALUES ('2000-01-06 12:00:00','BB',35)")
    c.execute("INSERT INTO price(Timestamp,symbol,price) VALUES ('2000-01-07 12:00:00','AA',80)")
    c.execute("INSERT INTO price(Timestamp,symbol,price) VALUES ('2000-01-07 12:00:00','BB',40)")
    c.execute("INSERT INTO trade(symbol,quantity,price) VALUES ('AA',10,90)")
    c.execute("INSERT INTO trade(symbol,quantity,price) VALUES ('AA',20,90)")
    c.execute("INSERT INTO trade(symbol,quantity,price) VALUES ('AA',-10,95)")
    c.execute("INSERT INTO shares(date,trans,symbol,qty,price) VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
    c.execute("INSERT INTO shares(date,trans,symbol,qty,price) VALUES ('2006-01-06','BUY','IBM',50,5.40)")

    db.commit()
    db.close()
    print 'initialise_db!! !!'

initialise_db()


def get_shares_data(db):
    return db.execute("SELECT symbol, sum(qty),-sum(price*qty) from shares group by symbol order by symbol").fetchall()

def get_shares(db):
    return db.execute("SELECT Id, Timestamp, symbol from share").fetchall()

def get_prices(db):
    return db.execute("SELECT Id, Timestamp, symbol,price from price").fetchall()

def get_trades(db):
    return db.execute("SELECT Id, Timestamp, symbol,quantity,price from trade").fetchall()

@app.before_request
def before_request():
    g.db = sqlite3.connect("shares.db")

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/price_insert', methods = ['POST'])
def price_insert():
    print 'Insert price'
    return redirect('/price_entry')

@app.route('/signup', methods = ['POST'])
def signup():
    try:
        share = request.form['share']
        qty = request.form['qty']
        price = request.form['price']
        side = request.form['side']
        print share, qty, price,side
  
        price = float(price)
        qty = int(qty)
        print 'xx', price
        if side == 'sell':
            qty = -qty

        sql = "INSERT INTO shares(date,trans,symbol,qty,price) VALUES ('2006-01-07','BUY','%s',%s,%s)" %(share,qty,price) 
        print 'sql:',sql
        g.db.execute(sql)
        g.db.commit()
        return redirect('/trade_entry')
    except Exception, e:
        print str(e)

@app.route('/price_entry')
def price_entry():
    return render_template('price_entry.html')

@app.route('/trade_entry')
def trade_entry():
    #return render_template('price_entry.html')
    return render_template('trade_entry.html')


@app.route('/data')
def data():
    shares_data = get_shares_data(g.db)
    shares = get_shares(g.db)
    prices = get_prices(g.db)
    trades = get_trades(g.db)
    return render_template('data.html', shares_data = shares_data, shares = shares, prices = prices, trades=trades )

@app.route('/view')
def view():
    shares_data = get_shares_data(g.db)
    j_shares_data = json.dumps(shares_data )
    x =  render_template('shares_chart.html')
    return x %str(j_shares_data)[1:-1]

@app.route('/view_prices')
def view_prices():
    #shares_data = get_shares_data(g.db)
    #j_shares_data = json.dumps(shares_data )
    #x =  render_template('prices_chart.html')

    shares = get_shares(g.db)
    prices = get_prices(g.db)
    trades = get_trades(g.db)

   
    share_symbols = []

    cols = " data.addColumn('datetime', 'Date'); \n "
    for share in shares:
          symbol = share[2]
          share_symbols.append(symbol)
 
          headers = " data.addColumn('number', '%s');  \n\
                      data.addColumn('string', '%s title'); \n\
                      data.addColumn('string', '%s text');  \n" \
                     %(symbol,symbol,symbol)

          cols += headers
   
     
    prices_data = '''
          [new Date(2314, 02, 15, 12, 00, 00), 12400.0, undefined, undefined, 10645, undefined, undefined],
          [new Date(2314, 2, 16, 12, 0, 0), 24045, 'AA Buy', '100', 12374, undefined, undefined],
          [new Date(2314, 2, 18, 12, 0, 0), 12284, 'AA Sell', '20', 30000, undefined, undefined ],
          [new Date(2314, 2, 17, 12, 30, 0), 15766 , 'A' , 'B', 16766, 'C', 'D'],
          [new Date(2314, 2, 19, 12, 0, 0), 8476, 'AA Sell', '5', 66467, 'BB Sell', '50'],
          [new Date(2314, 2, 19, 19, 0, 0), 8476, undefined, undefined , 66467, 'BB Sell', '50'],
          [new Date(2314, 2, 20, 12, 0, 0), 0, undefined, undefined, 55000, 'BB Sell', '150']
    '''
    print 'ORIG PRICES_DATA', prices_data

    price_data = {}

    # convert the sql data into a dictionary
    for price in prices:
         price_date = price[1]
         price_symbol = price[2]
         price_value = price[3]
         price_data.setdefault(price_date,{})
         price_data[price_date].setdefault(price_symbol,price_value)

    # start building up the data string
    prices_data_mh = '' 
   
    for date, values in price_data.items():
        tmp_date, tmp_time = date.split()
        YYYY, MM, DD = tmp_date.split('-')
        hh, mm, ss = tmp_time.split(':')
        
        prices_data_mh += '[new Date(%s, %s, %s, %s, %s, %s)' %(YYYY,MM,DD,hh,mm,ss)
        for share_symbol in share_symbols:
            prices_data_mh += ', %s, %s, %s' %( values.get(share_symbol,'undefined') ,'undefined','undefined ')
        prices_data_mh = prices_data_mh[:-1] 
        prices_data_mh += '],\n' 
  
    prices_data_mh = prices_data_mh[:-2] 
    print 'PRICE DATA NEW'
    print prices_data_mh 
  
 
    template =  render_template('prices_chart.html')
    return template %(cols,prices_data_mh)
    

@app.route('/')
def hello_world():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()


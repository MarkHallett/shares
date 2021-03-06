# play-trader.py

import os
import json
import sqlite3
from flask import Flask, render_template
from flask import request, redirect
from flask import g
import db_wrap.share
import db_wrap.trade
import db_wrap.price
import db_wrap.values

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
    db_wrap.share.create(c)
    db_wrap.price.create(c)
    db_wrap.trade.create(c)

    c.execute('''CREATE TABLE shares
             (Id integer PRIMARY KEY, date text, trans text, symbol text, qty real, price real)''')
    
    # Insert a start data
    db_wrap.share.insert_start_data(c)
    db_wrap.price.insert_start_data(c)
    db_wrap.trade.insert_start_data(c)

    db.commit()
    db.close()
    print 'initialise_db!! !!'

initialise_db()


def get_shares_data(db):
    return db.execute("SELECT symbol, sum(qty),-sum(price*qty) from shares group by symbol order by symbol").fetchall()

@app.before_request
def before_request():
    g.db = sqlite3.connect("shares.db")

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

def insert_trade():
    pass


@app.route('/trade_insert', methods = ['POST'])
def trade_insert():
    try:	
         symbol = request.form['share']
         quantity = int(request.form['quantity'])
         side = request.form['side']
         max_date = db_wrap.price.get_max_date(g.db)

         if side == 'sell':
             quantity *= -1

         price = db_wrap.price.get_share_price(g.db,max_date, symbol)
         print 'TRADE ENTRY',max_date, symbol, quantity, price
         db_wrap.trade.insert(g.db,max_date,symbol,quantity,price)
    except Exception, e:
         print "ERROR trade_insert, %s" %str(e)
    return redirect('/trader_view')

@app.route('/signup', methods = ['POST'])
def signup():
    try:
        share = request.form['share']
        qty = request.form['qty']
        price = request.form['price']
        side = request.form['side']
  
        price = float(price)
        qty = int(qty)
        if side == 'sell':
            qty = -qty

        sql = "INSERT INTO shares(date,trans,symbol,qty,price) VALUES ('2006-01-07','BUY','%s',%s,%s)" %(share,qty,price) 
        g.db.execute(sql)
        g.db.commit()
        return redirect('/trade_entry')
    except Exception, e:
        print str(e)

@app.route('/top_nav')
def top_nav():
    return render_template('top_nav.html')
      
@app.route('/trader_menu')
def trader_menu():
    return render_template('trader_menu.html')
      
@app.route('/support_menu')
def support_menu():
    return render_template('support_menu.html')
      
@app.route('/related_view1')
def related_view1():
    return value_view() 
      
@app.route('/related_view2')
def related_view2():
    return inventory_view() 
      
@app.route('/footer')
def footer():
    return render_template('footer.html')
      

@app.route('/trader_view')
def trader_view():
    share_entry = render_template('trader_view.html')
    tmp_view_prices = view_prices()
    return share_entry + tmp_view_prices

@app.route('/trade_entry')
def trade_entry():
    return render_template('trade_entry.html')

@app.route('/inventory_view')
def inventory_view():
    try:
        shares = db_wrap.trade.get_trades_inventory(g.db)
        j_shares = json.dumps(shares )
        x =  render_template('inventory_view.html')
        return x %str(j_shares)[1:-1]
    except Exception, e:
        print 'ERROR inventory_view %s' %(str(e))

    return render_template('inventory_view.html')

@app.route('/value_view')
def value_view():
    try:
        values  = db_wrap.values.get_values(g.db)
        x =  render_template('value_view.html')
    except Exception, e:
        print 'ERROR value_view %s' %str(e)
    return x %str(values)

    #return render_template('value_view.html')


@app.route('/data')
def data():
    shares = db_wrap.share.get_shares(g.db)
    trades = db_wrap.trade.get_trades(g.db)
    prices = db_wrap.price.get_prices(g.db)
    return render_template('data.html', shares = shares, prices = prices, trades=trades )

@app.route('/view')
def view():
    shares_data = get_shares_data(g.db)
    j_shares_data = json.dumps(shares_data )
    x =  render_template('shares_chart.html')
    return x %str(j_shares_data)[1:-1]

@app.route('/view_prices')
def view_prices():
    shares = db_wrap.share.get_shares(g.db)
    prices = db_wrap.price.get_prices(g.db)
    trades = db_wrap.trade.get_trades(g.db)

    trade_dates = {}
    for trade_data in trades:
        trade_id  = trade_data[0]
        trade_date = trade_data[1]
        trade_symbol = trade_data[2]
        trade_amount = trade_data[3]
        trade_price = trade_data[4]
        
        trade_dates.setdefault(trade_date,{})         
        trade_dates[trade_date].setdefault(trade_symbol,{})
        trade_dates[trade_date][trade_symbol] = (trade_id, trade_amount, trade_price )


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
  
    date_keys = price_data.keys()
    date_keys.sort()
 

    for date in date_keys:
        values = price_data[date]

        tmp_date, tmp_time = date.split()
        YYYY, MM, DD = tmp_date.split('-')
        hh, mm, ss = tmp_time.split(':')
        
        prices_data_mh += '[new Date(%s, %s, %s, %s, %s, %s)' %(YYYY,MM,DD,hh,mm,ss)
        for share_symbol in share_symbols:
            # add annotations
 
            if trade_dates.has_key(date) and trade_dates[date].has_key(share_symbol): 
                trade_id, trade_quantity,trade_price = trade_dates[date][share_symbol]
                if trade_quantity > 0 :
                    side = '(%s) Buy' %trade_id
                else:
                    side = '(%s) Sell' %trade_id
                msg2 = '%s %s @ %s' %(trade_quantity, share_symbol, trade_price)
                prices_data_mh += ", %s, '%s', '%s' " %( values.get(share_symbol,'undefined') ,side,msg2)
            else:
                prices_data_mh += ", %s, %s, %s " %( values.get(share_symbol,'undefined') ,'undefined','undefined ')
        prices_data_mh = prices_data_mh[:-1] 
        prices_data_mh += '],\n' 
  
    prices_data_mh = prices_data_mh[:-2] 
 
    template =  render_template('prices_chart.html')
    return template %(cols,prices_data_mh)
    

@app.route('/')
def hello_world():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()


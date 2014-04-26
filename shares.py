# shares.py

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

    # Create table
    c.execute('''CREATE TABLE shares
             (Id integer PRIMARY KEY, date text, trans text, symbol text, qty real, price real)''')

    # Insert a row of data
    c.execute("INSERT INTO shares(date,trans,symbol,qty,price) VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
    c.execute("INSERT INTO shares(date,trans,symbol,qty,price) VALUES ('2006-01-06','BUY','IBM',50,5.40)")

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
        return redirect('/entry')
    except Exception, e:
        print str(e)
@app.route('/entry')
def entry():
    return render_template('entry.html')



@app.route('/data')
def data():
    shares_data = get_shares_data(g.db)
    return render_template('data.html', shares_data = shares_data )

@app.route('/view')
def view():
    shares_data = get_shares_data(g.db)
    j_shares_data = json.dumps(shares_data )
    x =  render_template('shares_chart.html')
    return x %str(j_shares_data)[1:-1]

@app.route('/')
def hello_world():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()


# values.py
import sqlite3
import json
import price

def get_trades(db):
    return db.execute("SELECT Id, Timestamp, symbol,quantity,price from trade").fetchall()

def get_trades_inventory(db):
    return db.execute("SELECT symbol, sum(quantity) from trade group by symbol ").fetchall()

def get_cash_spent(db):
    sql = "select sum(quantity * -price) from trade"
    return db.execute(sql).fetchall()[0][0]
    
def get_shares_total_quantity(db):
    sql = "select symbol, sum(quantity) from trade group by symbol"
    results = db.execute(sql).fetchall()
    shares_total = {}
    for r in results:
        share = r[0]
        total = r[1]
        shares_total[share] = total
    return shares_total


def get_values(db):
    chart_items = []
    cash_spent = get_cash_spent(db)
    chart_items.append(('Cash', cash_spent))


    max_date = price.get_max_date(db)
    latest_prices_rtn  = price.get_share_prices(db, max_date )
    
    last_prices = {}
    for last_price in latest_prices_rtn: 
         share = last_price[0]
         share_price = last_price[1]
         last_prices[share] = share_price


    total_value = cash_spent
    shares_total_quantity = get_shares_total_quantity(db)
    for symbol, quantity in shares_total_quantity.items():
        value = quantity * last_prices[symbol] 
        chart_items.append((symbol, value))
        total_value += value

    chart_items.append(('Profit', total_value))
    return json.dumps(chart_items)[1:-1]
    

def test():
    print 'values.test'
    db = sqlite3.connect("../shares.db") 
    print "trades", get_trades(db)
    print "trades_inventory", get_trades_inventory(db)
    print "get_values", get_values(db)



if __name__ == '__main__':
    test()


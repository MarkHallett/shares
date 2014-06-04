# job.py

import time
import os
import sqlite3

# -- run table ---------------------------

def create(c):
    c.execute(''' CREATE TABLE run
                 ( status bool ) ''' )

def set_run_status(db,status):    
    sql = '''update run set status = "%s" ''' %status 
    status = db.execute(sql)
    db.commit()
    db.close()
    return 

def get_run_status(db):
    status = db.execute(''' select status from run''').fetchall()[0][0]
    return status


def get_runs(db):
    try: 
        rtn = db.execute("SELECT status from run").fetchall()
    except Exception, e:
        print 'Error run.get_runs: %s' %(str(e))        
        return []
    return rtn



# ---------------------------------------
def insert_start_data(c):
    print 'Inserting status into run'
    c.execute("INSERT INTO run(status) VALUES ('True')")




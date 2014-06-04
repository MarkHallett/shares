# job.py

import time
import os
import sqlite3

# -- worker table ---------------------------

def create(c):
    c.execute(''' CREATE TABLE worker
                 ( Id integer PRIMARY KEY,
                   Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                   name text ,
                   status text ) ''' )

def add_worker(db,name):    
    sql = '''INSERT into worker (name,status) VALUES ( '%s','Waiting') ''' %(name)
    status = db.execute(sql)
    db.commit()
    sql = 'SELECT min(Id) from worker'
    id = db.execute(sql).fetchall()[0][0]
    return id

def remove_worker(db,id):
    #status = db.execute(''' select status from run''').fetchall()[0][0]
    sql = ''' DELETE from worker where Id = %s ''' %(id)
    status = db.execute(sql)
    db.commit()
    return 

def set_status(db, name,status):
    return db.execute("UPDATE worker set status = '%s' where name = '%s'  " %(status,name))
    db.commit()
    return 

def get_workers(db):
    try:
        rtn = db.execute("SELECT * from worker").fetchall()
    except Exception, e:
        print 'Error run.get_runs: %s' %(str(e))
        return []
    print rtn
    return rtn
   



# ---------------------------------------
def insert_start_data(c):
    pass
    #print 'Inserting status into run'
    #c.execute("INSERT INTO run(status) VALUES ('True')")




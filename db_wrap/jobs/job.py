# job.py

import time
import os
import sys
import traceback
import sqlite3

# -- job table ---------------------------

def create(c):
    c.execute('''CREATE TABLE job 
             (Id integer PRIMARY KEY,
              Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
              name text,
              status text,
              start_proc datetime,
              who text,
              error_count int,
              end_proc datetime,
              end_status int   )''')


def update_job_ended(db,job_id,worker_id,status):
    #print 'update_job_ended', job_id, worker_id, status
    now = time.mktime( time.gmtime() )
    now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(now))

    c = db.cursor()
    # TODO if end in error +1 the error count
    sql = "UPDATE job set status = 'Finished', end_proc = '%s', end_status = %s  where Id = '%s' " %( now, status, job_id )
    c.execute(sql)
    sql = "UPDATE worker  set status = 'Waiting' where Id = '%s'" %( worker_id )
    c.execute(sql)
    db.commit()
    


def insert_job_getprice(db):
    c = db.cursor()
    sql = "INSERT into job(name,status) VALUES ('get_prices','Waiting')"
    print sql
    c.execute(sql)

def get_next_job(db, worker_id):
    try:
        # get details of the next job to run
        #print 'job.get_next_job'    
        sql =  "SELECT min(Id)  from job where status = 'Waiting' "
        next_job_id  = db.execute(sql).fetchall()[0][0]
        #print 'XXXX', next_job_id

        if next_job_id == None:
            next_job_name = None
        else:
            # the is work to be done!
            sql =  "SELECT name from job where Id = %s " %next_job_id
            next_job_name  = db.execute(sql).fetchall()[0][0]
            #print 'XXXX', next_job_name, type(next_job_name)

            # update the worker and the job 
            now = time.mktime( time.gmtime() )
            now = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(now))
            #print 'now', now
            sql = "UPDATE job set status = 'Running', start_proc = '%s' , who = %s where Id = '%s'" %( now ,worker_id, next_job_id )
            #print 'update job sql:', sql
            db.execute(sql)
            sql = "UPDATE worker  set status = 'Running' where Id = '%s'" %( worker_id )
            #print 'update job sql:', sql

        db.execute(sql)
        db.commit()
        db.close()
  
        return next_job_id, next_job_name
    except Exception, e:
        print ''.join(traceback.format_exception(*sys.exc_info())[-2:]).strip().replace('\n',': ') 
        print 'ERROR get_next_job: %s' %(str(e)) 
        return None,None

def start_prices(db):
    print 'Start prices'
    sql = " select * from job where name = 'get_prices' and status in ( 'Running' , 'Waiting' )  "
    print 'sql', sql
    res = db.execute(sql).fetchall()
    print 'res', res
    if res == []:
        insert_job_getprice(db)
    db.commit()
  

def get_jobs(db):
    return db.execute("SELECT Id, Timestamp, name, status, start_proc, who, error_count, end_proc, end_status from job").fetchall()     

# ---------------------------------------

if __name__ == '__main__':
    print 'running'

    print 'initialise_jobs!!'
    if os.path.isfile('../jobs.db'):
        print 'jobs.db exists'
        print 'insert job getprice'
        db = sqlite3.connect("../jobs.db")
        insert_job_getprice(db)
        db.commit()
        db.close()



    else:
      print 'jobs.db does not exists'
      db = sqlite3.connect("../jobs.db")

      c = db.cursor()

      # Create tables
      create_job(c)
      create_run(c)

      insert_start_data(c)

      db.commit()
      db.close()
      print 'initialised_jobs!! !!'





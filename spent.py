import sqlite3 as db
from datetime import datetime
def init():
    conn = db.connect("expense.db")
    cur = conn.cursor()
    sql = '''
    create table if not exists expense (
        amount number,
        category string,
        message string,
        date string
        )
    '''
    cur.execute(sql)
    conn.commit()

def log(amount, category, message = ""):
    date = str(datetime.now())
    conn = db.connect("expense.db")
    cur = conn.cursor()
    sql = '''
    insert into expense values (
         {},
        '{}',
        '{}',
        '{}'
    )
    '''.format(amount, category, message, date)
    cur.execute(sql)
    conn.commit()

def view(category=None):
    conn = db.connect("expense.db")
    cur = conn.cursor()
    if category:
        sql = '''
        select * from expense where category = '{}'
        '''.format(category)
        sql2 = '''
        select sum(amount) from expense where category = '{}'
        '''.format(category)
    else :
        sql = '''
        select * from expense
        '''
        sql2 = '''
        select sum(amount) from expense
        '''.format(category)
    cur.execute(sql)
    results = cur.fetchall()
    cur.execute(sql2)
    total_amount = cur.fetchone()[0]
    return results,total_amount
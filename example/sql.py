#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import sqlite3

sql = '''create table if not exists users(
    id integer primary key autoincrement,
    name varchar(30)
    )
'''


def fill_data():
    conn = sqlite3.connect('test.db')
    cur = conn.cursor()
    for i in range(300):
        cur.execute('insert into users (name) values (?)', ['name' + str(i)])

    conn.commit()
    conn.close()


def init_db():
    conn = sqlite3.connect('test.db')
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('python sql.py [init_db|fill_data]')
        print('init_db   => initialize database')
        print('fill_data => fill data for testing')
        sys.exit(0)

    action = sys.argv[1]
    if action == 'init_db':
        init_db()
    elif action == 'fill_data':
        fill_data()
    else:
        print('invalid choices, choose from [init_db, fill_data]')

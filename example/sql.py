#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import sqlite3

sql = '''create table if not exists users(
    id integer primary key autoincrement,
    name varchar(30)
    )
'''


def fill_data(total=300):
    conn = sqlite3.connect('test.db')
    cur = conn.cursor()
    for i in range(total):
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
        print('python sql.py [init_db|fill_data] [total_records]')
        print('init_db       => initialize database')
        print('fill_data     => fill data for testing')
        print('total_records => generate how many records, default is 300')
        sys.exit(0)

    action = sys.argv[1]
    if len(sys.argv) >= 3:
        total = sys.argv[2]
    else:
        total = 300

    if action == 'init_db':
        init_db()
    elif action == 'fill_data':
        fill_data(int(total))
    else:
        print('invalid choices, choose from [init_db, fill_data]')

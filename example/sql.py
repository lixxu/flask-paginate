#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import sqlite3
import click

click.disable_unicode_literals_warning = True

sql = '''create table if not exists users(
    id integer primary key autoincrement,
    name varchar(30)
    )
'''


@click.group()
def cli():
    pass


@cli.command(short_help='initialize database and tables')
def init_db():
    conn = sqlite3.connect('test.db')
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    conn.close()


@cli.command(short_help='fill records to database')
@click.option('--total', '-t', default=300, help='fill data for example')
def fill_data(total):
    conn = sqlite3.connect('test.db')
    cur = conn.cursor()
    for i in range(total):
        cur.execute('insert into users (name) values (?)', ['name' + str(i)])

    conn.commit()
    conn.close()


if __name__ == '__main__':
    cli()

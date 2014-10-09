#!/usr/bin/env python
#-*- coding: utf-8 -*-

from __future__ import unicode_literals
import sqlite3
from flask import Flask, render_template, g, current_app, request
from flask.ext.paginate import Pagination

app = Flask(__name__)
app.config.from_pyfile('app.cfg')


@app.before_request
def before_request():
    g.conn = sqlite3.connect('test.db')
    g.conn.row_factory = sqlite3.Row
    g.cur = g.conn.cursor()


@app.teardown_request
def teardown(error):
    if hasattr(g, 'conn'):
        g.conn.close()


@app.route('/')
def index():
    g.cur.execute('select count(*) from users')
    total = g.cur.fetchone()[0]
    page, per_page, offset = get_page_items()
    sql = 'select name from users order by name limit {}, {}'\
        .format(offset, per_page)
    g.cur.execute(sql)
    users = g.cur.fetchall()
    pagination = get_pagination(page=page,
                                per_page=per_page,
                                total=total,
                                record_name='users',
                                )
    return render_template('index.html', users=users,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )


def get_css_framework():
    return current_app.config.get('CSS_FRAMEWORK', 'bootstrap3')


def get_link_size():
    return current_app.config.get('LINK_SIZE', 'sm')


def show_single_page_or_not():
    return current_app.config.get('SHOW_SINGLE_PAGE', False)


def get_page_items():
    page = int(request.args.get('page', 1))
    per_page = request.args.get('per_page')
    if not per_page:
        per_page = current_app.config.get('PER_PAGE', 10)
    else:
        per_page = int(per_page)

    offset = (page - 1) * per_page
    return page, per_page, offset


def get_pagination(**kwargs):
    kwargs.setdefault('record_name', 'records')
    return Pagination(css_framework=get_css_framework(),
                      link_size=get_link_size(),
                      show_single_page=show_single_page_or_not(),
                      **kwargs
                      )

if __name__ == '__main__':
    app.run(debug=True)


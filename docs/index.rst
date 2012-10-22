Flask-Paginate |release| documentation
===========================================

.. module:: flaskext.paginate

Overview
---------
**Flask-Paginate** is an simple paginate extension for
`Flask`_ which is reference to `will_paginate`_,
and use twitter `bootstrap`_ as css framework.

**Note**: Flask-Paginate requires Python 2.6+ (use **string.format** syntax)

.. sourcecode:: html+jinja

    {{ pagination.info|safe }}

.. figure:: _static/paginate-info.png
    :alt: The screenshot of paginate information

or

.. figure:: _static/paginate-info2.png
    :alt: The screenshot of paginate information when search

.. sourcecode:: html+jinja

    {{ pagination.links|safe }}

.. figure:: _static/paginate-links.png
    :alt: The screenshot of paginate links

.. highlight:: bash

Installation
------------------------

Install the extension with one of the following commands:::

  $ easy_install flask-paginate

or alternatively if you have pip installed::

  $ pip install flask-paginate

Configuration
------------------

If you want to show the pagination information, add below lines to your
css file.

.. sourcecode:: css

    .pagination-page-info {
        padding: .6em;
        padding-left: 0;
        width: 40em;
        margin: .5em;
        margin-left: 0;
        font-size: 12px;
    }
    .pagination-page-info b {
        color: black;
        background: #6aa6ed;
        padding-left: 2px;
        padding: .1em .25em;
        font-size: 150%;
    }

How to use
------------
In your Flask views file (e.g. views/users.py)::

    from flask import Blueprint
    from flask.ext.paginate import Pagination

    mod = Blueprint('users', __name__)


    @mod.route('/')
    def index():
        search = False
        q = request.args.get('q')
        if q:
            search = True

        users = User.find(...)
        pagination = Pagination(users.count, search=search)
        return render_template('users/index.html',
                               users=users,
                               pagination=pagination,
                               )

In the **users/index.html**:

.. sourcecode:: html+jinja

    {{ pagination.info|safe }}
    {{ pagination.links|safe }}
    <table>
      <thead>
        <tr>
          <th>#</th>
          <th>Name</th>
          <th>Email</th>
        </tr>
      </thead>
      <tbody>
        {% for user in users %}
          <tr>
            <td>{{ loop.index }}</td>
            <td>{{ user.name }}</td>
            <td>{{ user.email }}</td>
          </tr>
        {% endfor %}
      </tbody>
    </table>
    {{ pagination.links|safe }}

Deep into the Pagination
--------------------------

Below are the params for **Paginate.__init__()**, you can change the settings here.

    **found**: is used when searching

    **page**: current page

    **per_page**: how many items displayed on one page

    **inner_window**: how many links arround current page

    **outer_window**: how many links near first/last link

    **prev_label**: text for previous page, default is **&laquo;**

    **next_label**: text for next page, default is **&raquo;**

    **search**: search or not?

    **total**: total records for pagination

    **display_msg**: text for pagation information

    **search_msg**: text for search information

API
------------------

.. autoclass:: Pagination
   :members:

.. toctree::
   :maxdepth: 2

.. _Flask: http://flask.pocoo.org/
.. _will_paginate: https://github.com/mislav/will_paginate/wiki
.. _bootstrap: http://twitter.github.com/bootstrap/

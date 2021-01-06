flask-paginate
==============

Pagination support for flask framework (study from will_paginate).
It supports several css frameworks.
It requires Python2.6+ as string.format syntax.

If you want to show pagination-info
("Total <b>100</b> posts, displaying <b>20 - 30</b>")
above the pagination links,
please add the below lines to your css file::

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

Full documentation: <http://flask-paginate.readthedocs.io>

Run example:

    $cd example
    $python sql.py
    $python sql.py init_db
    $python sql.py fill_data --total=310
    $cp app.cfg.example app.cfg
    $echo edit app.cfg
    $python app.py --port 5000

Open <http://localhost:5000> to see the example page.

![demo](/example/demo.png "demo")

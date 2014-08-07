flask-paginate
==============

Paginate support for flask framework (study from will_paginate).
Use bootstrap for css framework
It requires Python2.6+ as string.format syntax.

If you want to show pagination-info
("Total <b>100</b> posts, displaying <b>20 - 30</b>")
above the pagination links,
please add below lines to your css file::

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

Full documention: <http://pythonhosted.org/Flask-paginate/>

Run example:

    $cd example
    $python sql.py init_db
    $python sql.py fill_data
    $python app.py

Open <http://localhost:5000> to see the example page.

![demo](https://github.com/lixxu/flask-paginate/tree/master/example/demo.png "demo") 

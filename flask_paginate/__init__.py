#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    flask_paginate
    ~~~~~~~~~~~~~~~~~~

    Adds pagination support to your application.

    :copyright: (c) 2013 by Lix Xu.
    :license: BSD, see LICENSE for more details
"""

from __future__ import unicode_literals
import sys
from flask import request, url_for, Markup, current_app

__version__ = '0.5.5'

PY2 = sys.version_info[0] == 2

_bs = '<li class="previous"><a href="{0}">{1}</a></li>'
_bs33 = '<li><a href="{0}" aria-label="Previous">\
<span aria-hidden="true">{1}</span></a></li>'
_bs4 = '<li class="page-item">\
<a class="page-link" href="{0}" aria-label="Previous">\
<span aria-hidden="true">{1}</span>\
<span class="sr-only">Previous</span></a></li>'
PREV_PAGES = dict(bootstrap=_bs,
                  bootstrap2=_bs,
                  bootstrap3=_bs,
                  bootstrap3_3=_bs33,
                  bootstrap4=_bs4,
                  semantic='<a class="item arrow" href="{0}">{1}</a>',
                  foundation='<li class="arrow"><a href="{0}">{1}</a></li>',
                  )

_bs = '<li class="next"><a href="{0}">{1}</a></li>'
_bs33 = '<li><a href="{0}" aria-label="Next">\
<span aria-hidden="true">{1}</span></a></li>'
_bs4 = '<li class="page-item">\
<a class="page-link" href="{0}" aria-label="Next">\
<span aria-hidden="true">{1}</span>\
<span class="sr-only">Next</span></a></li>'
NEXT_PAGES = dict(bootstrap=_bs,
                  bootstrap2=_bs,
                  bootstrap3=_bs,
                  bootstrap3_3=_bs33,
                  bootstrap4=_bs4,
                  semantic='<a class="item arrow" href="{0}">{1}</a>',
                  foundation='<li class="arrow"><a href="{0}">{1}</a></li>',
                  )

_bs = '<li class="active"><a>{0}</a></li>'
_bs33 = '<li class="active"><span>{0} \
<span class="sr-only">(current)</span></span></li>'
_bs4 = '<li class="page-item active"><a class="page-link">{0} \
<span class="sr-only">(current)</span></a></li>'
CURRENT_PAGES = dict(bootstrap=_bs,
                     bootstrap2=_bs,
                     bootstrap3=_bs,
                     bootstrap3_3=_bs33,
                     bootstrap4=_bs4,
                     semantic='<a class="item active">{0}</a>',
                     foundation='<li class="current"><a>{0}</a></li>',
                     )

LINK = '<li><a href="{0}">{1}</a></li>'
SEMANTIC_LINK = '<a class="item" href="{0}">{1}</a>'
BS4_LINK = '<li class="page-item"><a class="page-link" href="{0}">{1}</a></li>'

_bs = '<li class="disabled"><a>...</a></li>'
_bs33 = '<li class="disabled"><span>\
<span aria-hidden="true">...</span></span></li>'
_bs4 = '<li class="page-item disabled"><span class="page-link">...</span></li>'
_se = '<a class="disabled item">...</a>'
_fa = '<li class="unavailable"><a>...</a></li>'
GAP_MARKERS = dict(bootstrap=_bs,
                   bootstrap2=_bs,
                   bootstrap3=_bs,
                   bootstrap3_3=_bs33,
                   bootstrap4=_bs4,
                   semantic=_se,
                   foundation=_fa,
                   )

_bs = '<li class="previous disabled unavailable"><a> {0} </a></li>'
_bs33 = '<li class="disabled"><span>\
<span aria-hidden="true">{0}</span></span></li>'
_bs4 = '<li class="page-item disabled"><span class="page-link"> {0} \
</span></li>'
_se = '<a class="item arrow disabled">{0}</a>'
_fa = '<li class="unavailable"><a>{0}</a></li>'
PREV_DISABLED_PAGES = dict(bootstrap=_bs,
                           bootstrap2=_bs,
                           bootstrap3=_bs,
                           bootstrap3_3=_bs33,
                           bootstrap4=_bs4,
                           semantic=_se,
                           foundation=_fa,
                           )

_bs = '<li class="next disabled"><a> {0} </a></li>'
_bs33 = '<li class="disabled"><span>\
<span aria-hidden="true">{0}</span></span></li>'
_bs4 = '<li class="page-item disabled"><span class="page-link"> {0} \
</span></li>'
_se = '<a class="item arrow disabled">{0}</a>'
_fa = '<li class="unavailable"><a>{0}</a></li>'
NEXT_DISABLED_PAGES = dict(bootstrap=_bs,
                           bootstrap2=_bs,
                           bootstrap3=_bs,
                           bootstrap3_3=_bs33,
                           bootstrap4=_bs4,
                           semantic=_se,
                           foundation=_fa,
                           )

PREV_LABEL = '&laquo;'
NEXT_LABEL = '&raquo;'
RECORD_NAME = 'records'

DISPLAY_MSG = '''displaying <b>{start} - {end}</b> {record_name} in
total <b>{total}</b>'''

SEARCH_MSG = '''found <b>{found}</b> {record_name},
displaying <b>{start} - {end}</b>'''

_bs4 = '<nav aria-label="..."><ul class="pagination{0}{1}">'
_bs33 = '<nav aria-label="..."><ul class="pagination{0}{1}">'
CSS_LINKS = dict(bootstrap='<div class="pagination{0}{1}"><ul>',
                 bootstrap2='<div class="pagination{0}{1}"><ul>',
                 bootstrap3='<ul class="pagination{0}{1}">',
                 bootstrap3_3=_bs33,
                 bootstrap4=_bs4,
                 semantic='<div class="ui pagination menu">',
                 foundation='<ul class="pagination{0}{1}">',
                 )
CSS_LINKS_END = dict(bootstrap='</ul></div>',
                     bootstrap2='</ul></div>',
                     bootstrap3='</ul>',
                     bootstrap3_3='</ul></nav>',
                     bootstrap4='</ul></nav>',
                     semantic='</div>',
                     foundation='</ul>',
                     )

# foundation aligment
F_ALIGNMENT = '<div class="pagination-{0}">'


def get_parameter(param=None, args=None, default='page'):
    if not args:
        args = request.args.copy()
        args.update(request.view_args.copy())

    if not param:
        pk = 'page_parameter' if default == 'page' else 'per_page_parameter'
        param = args.get(pk)
        if not param:
            param = current_app.config.get(pk.upper())

    return param or default


def get_page_parameter(param=None, args=None):
    return get_parameter(param, args, 'page')


def get_per_page_parameter(param=None, args=None):
    return get_parameter(param, args, 'per_page')


def get_page_args(page_parameter=None, per_page_parameter=None,
                  for_test=False):
    '''param order: 1. passed parameter 2. request.args 3: config value
    for_test will return page_parameter and per_page_parameter'''
    args = request.args.copy()
    args.update(request.view_args.copy())

    page_name = get_page_parameter(page_parameter, args)
    per_page_name = get_per_page_parameter(per_page_parameter, args)
    if for_test:
        return page_name, per_page_name

    page = int(args.get(page_name, 1))
    per_page = args.get(per_page_name)
    if not per_page:
        per_page = current_app.config.get(per_page_name.upper(), 10)
    else:
        per_page = int(per_page)

    offset = (page - 1) * per_page
    return page, per_page, offset


class Pagination(object):
    """A simple pagination extension for flask."""

    def __init__(self, found=0, **kwargs):
        '''Detail parameters.

            **found**: used when searching

            **page**: current page

            **per_page**: how many records displayed on one page

            **page_parameter**: a name(string) of a GET parameter that holds \
            a page index, Use it if you want to iterate over multiple \
            Pagination objects simultaniously.
            default is 'page'.

            **per_page_parameter**: a name for per_page likes page_parameter.
            default is 'per_page'.

            **inner_window**: how many links arround current page

            **outer_window**: how many links near first/last link

            **prev_label**: text for previous page, default is **&laquo;**

            **next_label**: text for next page, default is **&raquo;**

            **search**: search or not?

            **total**: total records for pagination

            **display_msg**: text for pagation information

            **search_msg**: text for search information

            **record_name**: record name showed in pagination information

            **link_size**: font size of page links

            **alignment**: the alignment of pagination links

            **href**: Add custom href for links - this supports forms \
            with post method. It MUST contain {0} to format page number

            **show_single_page**: decide whether or not a single page \
            returns pagination

            **bs_version**: the version of bootstrap, default is **2**

            **css_framework**: the css framework, default is **bootstrap**

            **anchor**: anchor parameter, appends to page href

            **format_total**: number format total, like **1,234**, \
            default is False

            **format_number**: number format start and end, like **1,234**, \
            default is False

            **url_coding**: coding for url encoding, default is **utf-8**

        '''
        self.found = found
        page_parameter = kwargs.get('page_parameter')
        if not page_parameter:
            page_parameter = get_page_parameter()

        self.page_parameter = page_parameter
        self.page = kwargs.get(self.page_parameter, 1)
        per_page_param = kwargs.get('per_page_parameter')
        if not per_page_param:
            per_page_param = get_per_page_parameter()

        self.per_page_parameter = per_page_param
        self.per_page = kwargs.get(per_page_param, 10)
        self.skip = (self.page - 1) * self.per_page
        self.inner_window = kwargs.get('inner_window', 2)
        self.outer_window = kwargs.get('outer_window', 1)
        self.prev_label = kwargs.get('prev_label') or PREV_LABEL
        self.next_label = kwargs.get('next_label') or NEXT_LABEL
        self.search = kwargs.get('search', False)
        self.total = kwargs.get('total', 0)
        self.format_total = kwargs.get('format_total', False)
        self.format_number = kwargs.get('format_number', False)
        self.url_coding = kwargs.get("url_coding", "utf-8")
        self.display_msg = kwargs.get('display_msg') or DISPLAY_MSG
        self.search_msg = kwargs.get('search_msg') or SEARCH_MSG
        self.record_name = kwargs.get('record_name') or RECORD_NAME
        self.css_framework = kwargs.get('css_framework', 'bootstrap').lower()
        if self.css_framework not in CURRENT_PAGES:
            self.css_framework = 'bootstrap'

        self.bs_version = kwargs.get('bs_version') or 2
        if self.css_framework.startswith('bootstrap'):
            if self.bs_version in (3, '3'):
                self.css_framework = 'bootstrap3'
            elif self.bs_version in ("3.3", "3_3"):
                self.css_framework = "bootstrap3_3"
            elif self.bs_version in (4, '4'):
                self.css_framework = 'bootstrap4'

        self.link_size = kwargs.get('link_size', '')
        if self.link_size:
            if self.css_framework == 'foundation':
                self.link_size = ''
            else:
                self.link_size = ' pagination-{0}'.format(self.link_size)

        self.alignment = kwargs.get('alignment', '')
        if self.alignment and self.css_framework.startswith('bootstrap'):
            if self.css_framework == 'bootstrap4':
                if self.alignment == 'center':
                    self.alignment = ' justify-content-center'
                elif self.alignment in ('right', 'end'):
                    self.alignment = ' justify-content-end'

            elif self.css_framework == "bootstrap2":
                self.alignment = ' pagination-{0}'.format(self.alignment)
            else:
                # v3 does not support this way
                # use this way: <div class="text-center/right">...</div>
                self.alignment = ''

        self.href = kwargs.get('href', None)
        self.anchor = kwargs.get('anchor', None)
        self.show_single_page = kwargs.get('show_single_page', False)

        self.link = LINK
        if self.css_framework == 'bootstrap4':
            self.link = BS4_LINK
        elif self.css_framework == 'semantic':
            self.link = SEMANTIC_LINK

        self.current_page_fmt = CURRENT_PAGES[self.css_framework]
        self.link_css_fmt = CSS_LINKS[self.css_framework]
        self.gap_marker_fmt = GAP_MARKERS[self.css_framework]
        self.prev_disabled_page_fmt = PREV_DISABLED_PAGES[self.css_framework]
        self.next_disabled_page_fmt = NEXT_DISABLED_PAGES[self.css_framework]
        self.prev_page_fmt = PREV_PAGES[self.css_framework]
        self.next_page_fmt = NEXT_PAGES[self.css_framework]
        self.css_end_fmt = CSS_LINKS_END[self.css_framework]
        self.init_values()

    def page_href(self, page):
        if self.href:
            url = self.href.format(page or 1)
        else:
            self.args[self.page_parameter] = page
            if self.anchor:
                url = url_for(self.endpoint, _anchor=self.anchor, **self.args)
            else:
                url = url_for(self.endpoint, **self.args)

        # Need to return a unicode object
        if self.url_coding:
            return url.decode(self.url_coding) if PY2 else url

        return url

    def init_values(self):
        current_total = self.found if self.search else self.total
        pages = divmod(current_total, self.per_page)
        self.total_pages = pages[0] + 1 if pages[1] else pages[0]
        self.has_prev = self.page > 1
        self.has_next = self.page < self.total_pages

        args = request.args.copy()
        args.update(request.view_args.copy())
        self.args = {}
        for k, v in args.lists():
            if len(v) == 1:
                self.args[k] = v[0]
            else:
                self.args[k] = v

        self.endpoint = request.endpoint

    @property
    def prev_page(self):
        if self.has_prev:
            page = self.page - 1 if self.page > 2 else None
            url = self.page_href(page)
            return self.prev_page_fmt.format(url, self.prev_label)

        return self.prev_disabled_page_fmt.format(self.prev_label)

    @property
    def next_page(self):
        if self.has_next:
            url = self.page_href(self.page + 1)
            return self.next_page_fmt.format(url, self.next_label)

        return self.next_disabled_page_fmt.format(self.next_label)

    @property
    def first_page(self):
        # current page is first page
        if self.has_prev:
            return self.link.format(self.page_href(None), 1)

        return self.current_page_fmt.format(1)

    @property
    def last_page(self):
        if self.has_next:
            url = self.page_href(self.total_pages)
            return self.link.format(url, self.total_pages)

        return self.current_page_fmt.format(self.page)

    @property
    def pages(self):
        if self.total_pages < self.inner_window * 2 - 1:
            return range(1, self.total_pages + 1)

        pages = []
        win_from = self.page - self.inner_window
        win_to = self.page + self.inner_window
        if win_to > self.total_pages:
            win_from -= win_to - self.total_pages
            win_to = self.total_pages

        if win_from < 1:
            win_to = win_to + 1 - win_from
            win_from = 1
            if win_to > self.total_pages:
                win_to = self.total_pages

        if win_from > self.inner_window:
            pages.extend(range(1, self.outer_window + 1 + 1))
            pages.append(None)
        else:
            pages.extend(range(1, win_to + 1))

        if win_to < self.total_pages - self.inner_window + 1:
            if win_from > self.inner_window:
                pages.extend(range(win_from, win_to + 1))

            pages.append(None)
            if self.outer_window == 0:
                pages.extend(range(self.total_pages, self.total_pages + 1))
            else:
                pages.extend(range(self.total_pages - 1, self.total_pages + 1))

        elif win_from > self.inner_window:
            pages.extend(range(win_from, self.total_pages + 1))
        else:
            pages.extend(range(win_to + 1, self.total_pages + 1))

        return pages

    def single_page(self, page):
        if page == self.page:
            return self.current_page_fmt.format(page)

        if page == 1:
            return self.first_page

        if page == self.total_pages:
            return self.last_page

        return self.link.format(self.page_href(page), page)

    def _get_single_page_link(self):
        s = [self.link_css_fmt.format(self.link_size, self.alignment)]
        s.append(self.prev_page)
        s.append(self.single_page(1))
        s.append(self.next_page)
        s.append(self.css_end_fmt)
        if self.css_framework == 'foundation' and self.alignment:
            s.insert(0, F_ALIGNMENT.format(self.alignment))
            s.append('</div>')

        return Markup(''.join(s))

    @property
    def links(self):
        """Get all the pagination links."""
        if self.total_pages <= 1:
            if self.show_single_page:
                return self._get_single_page_link()

            return ''

        s = [self.link_css_fmt.format(self.link_size, self.alignment)]
        s.append(self.prev_page)
        for page in self.pages:
            s.append(self.single_page(page) if page else self.gap_marker_fmt)

        s.append(self.next_page)
        s.append(self.css_end_fmt)
        if self.css_framework == 'foundation' and self.alignment:
            s.insert(0, F_ALIGNMENT.format(self.alignment))
            s.append('</div>')

        return Markup(''.join(s))

    @property
    def info(self):
        """Get the pagination information."""
        start = 1 + (self.page - 1) * self.per_page
        end = start + self.per_page - 1
        if end > self.total:
            end = self.total if not self.search else self.found

        if start > self.total:
            start = self.total if not self.search else self.found

        s = ['<div class="pagination-page-info">']
        page_msg = self.search_msg if self.search else self.display_msg
        if self.format_total:
            total_text = '{0:,}'.format(self.total)
        else:
            total_text = '{0}'.format(self.total)

        if self.format_number:
            start_text = '{0:,}'.format(start)
            end_text = '{0:,}'.format(end)
        else:
            start_text = start
            end_text = end

        s.append(page_msg.format(found=self.found,
                                 total=total_text,
                                 start=start_text,
                                 end=end_text,
                                 record_name=self.record_name,
                                 )
                 )
        s.append('</div>')
        return Markup(''.join(s))

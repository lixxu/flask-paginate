#!/usr/bin/env python
#-*- coding: utf-8 -*-

"""
    flask.ext.paginate
    ~~~~~~~~~~~~~~

    Adds pagination support to your application.

    :copyright: (c) 2013 by Lix Xu.
    :license: BSD, see LICENSE for more details
"""

from __future__ import unicode_literals
from flask import request, url_for

PREV_PAGE = '<li><a href="{0}">{1}</a></li>'
NEXT_PAGE = '<li><a href="{0}">{1}</a></li>'
ACTIVE_PAGE = '<li class="active"><a href="#">{0}</a></li>'
LINK = '<li><a href="{0}">{1}</a></li>'
GAP_MARKER = '<li class="disabled"><a href="#">...</a></li>'
DISABLED_PAGE = '<li class="disabled"><a href="#">{0}</a></li>'

PREV_LABEL = ' &laquo; '
NEXT_LABEL = ' &raquo; '
RECORD_NAME = 'records'

DISPLAY_MSG = '''Displaying <b>{start} - {end}</b> {record_name} in total
<b>{total}</b>'''

SEARCH_MSG = '''Found <b>{found}</b> {record_name} in total <b>{total}</b>,
displaying <b>{start} - {end}</b>'''

LINK_CSS = '<div class="pagination{0}{1}"><ul>'
BS3_LINK_CSS = '<ul class="pagination{0}{1}">'


class Pagination(object):
    '''A simple pagination extension for flask
    '''
    def __init__(self, found=0, **kwargs):
        '''provides the params:

            **found**: used when searching

            **page**: current page

            **per_page**: how many links displayed on one page

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

            **bs_version**: the version of bootstrap, default is **2**
        '''
        self.found = found
        self.page = kwargs.get('page', 1)
        self.per_page = kwargs.get('per_page', 10)
        self.inner_window = kwargs.get('inner_window', 2)
        self.outer_window = kwargs.get('outer_window', 1)
        self.prev_label = kwargs.get('prev_label') or PREV_LABEL
        self.next_label = kwargs.get('next_label') or NEXT_LABEL
        self.search = kwargs.get('search', False)
        self.total = kwargs.get('total', 0)
        self.display_msg = kwargs.get('display_msg') or DISPLAY_MSG
        self.search_msg = kwargs.get('search_msg') or SEARCH_MSG
        self.record_name = kwargs.get('record_name') or RECORD_NAME
        self.link_size = kwargs.get('link_size', '')
        if self.link_size:
            self.link_size = ' pagination-{0}'.format(self.link_size)

        self.alignment = kwargs.get('alignment', '')
        if self.alignment:
            self.alignment = ' pagination-{0}'.format(self.alignment)

        self.bs_version = kwargs.get('bs_version') or 2

    @property
    def total_pages(self):
        pages = divmod(self.total, self.per_page)
        return pages[0] + 1 if pages[1] else pages[0]

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.total_pages

    @property
    def endpoint(self):
        return request.endpoint

    @property
    def args(self):
        args = dict(request.args.to_dict().items() + request.view_args.items())
        args.pop('page', None)
        return args

    @property
    def prev_page(self):
        if self.has_prev:
            page = self.page - 1 if self.page > 2 else None
            return PREV_PAGE.format(url_for(self.endpoint,
                                            page=page,
                                            **self.args
                                            ),
                                    self.prev_label
                                    )

        return DISABLED_PAGE.format(self.prev_label)

    @property
    def next_page(self):
        if self.has_next:
            return NEXT_PAGE.format(url_for(self.endpoint,
                                            page=self.page + 1,
                                            **self.args
                                            ),
                                    self.next_label
                                    )

        return DISABLED_PAGE.format(self.next_label)

    @property
    def first_page(self):
        # current page is first page
        if self.has_prev:
            return LINK.format(url_for(self.endpoint, **self.args), 1)

        return ACTIVE_PAGE.format(1)

    @property
    def last_page(self):
        if self.has_next:
            return LINK.format(url_for(self.endpoint,
                                       page=self.total_pages,
                                       **self.args
                                       ),
                               self.total_pages
                               )

        return ACTIVE_PAGE.format(self.page)

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
            pages.extend(range(self.total_pages - 1, self.total_pages + 1))
        elif win_from > self.inner_window:
            pages.extend(range(win_from, self.total_pages + 1))
        else:
            pages.extend(range(win_to + 1, self.total_pages + 1))

        return pages

    def single_page(self, page):
        if page == self.page:
            return ACTIVE_PAGE.format(page)

        if page == 1:
            return self.first_page

        if page == self.total_pages:
            return self.last_page

        return LINK.format(url_for(self.endpoint, page=page, **self.args),
                           page
                           )

    @property
    def links(self):
        '''get all the pagination links'''
        if self.total_pages <= 1:
            return ''

        if self.bs_version == 3:
            s = [BS3_LINK_CSS.format(self.link_size, self.alignment)]
        else:
            s = [LINK_CSS.format(self.link_size, self.alignment)]

        s.append(self.prev_page)
        for page in self.pages:
            s.append(self.single_page(page) if page else GAP_MARKER)

        s.append(self.next_page)
        if self.bs_version == 3:
            s.append('</ul>')
        else:
            s.append('</ul></div>')

        return ''.join(s)

    @property
    def info(self):
        '''get the pagination information'''
        start = 1 + (self.page - 1) * self.per_page
        end = start + self.per_page - 1
        if end > self.total:
            end = self.total if not self.search else self.found

        if start > self.total:
            start = self.total if not self.search else self.found

        s = ['<div class="pagination-page-info">']
        page_msg = self.search_msg if self.search else self.display_msg
        s.append(page_msg.format(found=self.found,
                                 total=self.total,
                                 start=start,
                                 end=end,
                                 record_name=self.record_name,
                                 )
                 )
        s.append('</div>')
        return ''.join(s)

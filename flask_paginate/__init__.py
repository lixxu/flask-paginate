#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
flask_paginate
~~~~~~~~~~~~~~~~~~

Adds pagination support to your flask application.

:copyright: (c) 2012 by Lix Xu.
:license: BSD, see LICENSE for more details
"""

from __future__ import unicode_literals

import sys

from flask import current_app, request, url_for
from markupsafe import Markup

__version__ = "2024.04.12"

PY2 = sys.version_info[0] == 2

# previous link
_bs = '<li class="previous"><a href="{0}"{2}>{1}</a></li>'
_bs33 = '<li><a href="{0}" aria-label="Previous"{2}>\
<span aria-hidden="true">{1}</span></a></li>'
_bs4 = '<li class="page-item">\
<a class="page-link" href="{0}" aria-label="Previous"{2}>\
<span aria-hidden="true">{1}</span>\
<span class="sr-only">Previous</span></a></li>'
_bs5 = '<li class="page-item">\
<a class="page-link" href="{0}" aria-label="Previous"{2}>\
<span aria-hidden="true">{1}</span></a></li>'
_bulma = '<a class="pagination-previous" href="{0}" aria-label="Previous"{2}>{1}</a>'
_materialize = '<li class="waves-effect"><a href="{0}"{1}>\
<i class="material-icons">chevron_left</i></a></li>'

PREV_PAGES = dict(
    bootstrap=_bs,
    bootstrap2=_bs,
    bootstrap3=_bs,
    bootstrap3_3=_bs33,
    bootstrap4=_bs4,
    bootstrap5=_bs5,
    semantic='<a class="item arrow" href="{0}"{2}>{1}</a>',
    foundation='<li class="arrow"><a href="{0}"{2}>{1}</a></li>',
    bulma=_bulma,
    materialize=_materialize,
)

# next link
_bs = '<li class="next"><a href="{0}"{2}>{1}</a></li>'
_bs33 = '<li><a href="{0}" aria-label="Next"{2}>\
<span aria-hidden="true">{1}</span></a></li>'
_bs4 = '<li class="page-item">\
<a class="page-link" href="{0}" aria-label="Next"{2}>\
<span aria-hidden="true">{1}</span>\
<span class="sr-only">Next</span></a></li>'
_bs5 = '<li class="page-item">\
<a class="page-link" href="{0}" aria-label="Next"{2}>\
<span aria-hidden="true">{1}</span></a></li>'
_bulma = '<a class="pagination-next" href="{0}" aria-label="Next"{2}>{1}</a>'
_materialize = '<li class="waves-effect"><a href="{0}"{1}>\
<i class="material-icons">chevron_right</i></a></li>'
NEXT_PAGES = dict(
    bootstrap=_bs,
    bootstrap2=_bs,
    bootstrap3=_bs,
    bootstrap3_3=_bs33,
    bootstrap4=_bs4,
    bootstrap5=_bs5,
    semantic='<a class="item arrow" href="{0}"{2}>{1}</a>',
    foundation='<li class="arrow"><a href="{0}"{2}>{1}</a></li>',
    bulma=_bulma,
    materialize=_materialize,
)

# current page
_bs = '<li class="active"><a>{0}</a></li>'
_bs33 = '<li class="active"><span>{0} \
<span class="sr-only">(current)</span></span></li>'
_bs4 = '<li class="page-item active"><a class="page-link">{0} \
<span class="sr-only">(current)</span></a></li>'
_bs5 = '<li class="page-item active" aria-current="page">\
<span class="page-link">{0}</span></li>'
_bulma = '<li><a class="pagination-link is-current" aria-current="page">\
{0}</a></li>'
_materialize = '<li class="active"><a href="#!">{0}</a></li>'
CURRENT_PAGES = dict(
    bootstrap=_bs,
    bootstrap2=_bs,
    bootstrap3=_bs,
    bootstrap3_3=_bs33,
    bootstrap4=_bs4,
    bootstrap5=_bs5,
    semantic='<a class="item active">{0}</a>',
    foundation='<li class="current"><a>{0}</a></li>',
    bulma=_bulma,
    materialize=_materialize,
)

# normal link
LINK = '<li><a href="{0}">{1}</a></li>'
SEMANTIC_LINK = '<a class="item" href="{0}">{1}</a>'
BS4_LINK = '<li class="page-item"><a class="page-link" href="{0}">{1}</a></li>'
BS5_LINK = '<li class="page-item"><a class="page-link" href="{0}">{1}</a></li>'
BULMA_LINK = '<li><a class="pagination-link" href="{0}">{1}</a></li>'
MATERIALIZE_LINK = '<li><a class="waves-effect" href="{0}">{1}</a></li>'

# disabled link
_bs = '<li class="disabled"><a>...</a></li>'
_bs33 = '<li class="disabled"><span>\
<span aria-hidden="true">...</span></span></li>'
_bs4 = '<li class="page-item disabled"><span class="page-link">...</span></li>'
_bs5 = '<li class="page-item disabled"><span class="page-link">...</span></li>'
_se = '<a class="disabled item">...</a>'
_fa = '<li class="unavailable"><a>...</a></li>'
_bulma = '<li><span class="pagination-ellipsis">&hellip;</span></li>'
_materialize = '<li class="disabled"><a>...</a></li>'
GAP_MARKERS = dict(
    bootstrap=_bs,
    bootstrap2=_bs,
    bootstrap3=_bs,
    bootstrap3_3=_bs33,
    bootstrap4=_bs4,
    bootstrap5=_bs5,
    semantic=_se,
    foundation=_fa,
    bulma=_bulma,
    materialize=_materialize,
)

# previous disabled link
_bs = '<li class="previous disabled unavailable"><a> {0} </a></li>'
_bs33 = '<li class="disabled"><span>\
<span aria-hidden="true">{0}</span></span></li>'
_bs4 = '<li class="page-item disabled"><span class="page-link"> {0} \
</span></li>'
_bs5 = '<li class="page-item disabled">\
<a class="page-link">{0}</a></li>'
_se = '<a class="item arrow disabled">{0}</a>'
_fa = '<li class="unavailable"><a>{0}</a></li>'
_bulma = '<a class="pagination-previous" disabled>{0}</a>'
_materialize = '<li class="disabled"><a href="#!">\
<i class="material-icons">chevron_left</i></a></li>'
PREV_DISABLED_PAGES = dict(
    bootstrap=_bs,
    bootstrap2=_bs,
    bootstrap3=_bs,
    bootstrap3_3=_bs33,
    bootstrap4=_bs4,
    bootstrap5=_bs5,
    semantic=_se,
    foundation=_fa,
    bulma=_bulma,
    materialize=_materialize,
)

# next disabled link
_bs = '<li class="next disabled"><a> {0} </a></li>'
_bs33 = '<li class="disabled"><span>\
<span aria-hidden="true">{0}</span></span></li>'
_bs4 = '<li class="page-item disabled"><span class="page-link"> {0} \
</span></li>'
_bs5 = '<li class="page-item disabled">\
<a class="page-link">{0}</a></li>'
_se = '<a class="item arrow disabled">{0}</a>'
_fa = '<li class="unavailable"><a>{0}</a></li>'
_bulma = '<a class="pagination-next" disabled>{0}</a>'
_materialize = '<li class="disabled"><a href="#!">\
<i class="material-icons">chevron_right</i></a></li>'
NEXT_DISABLED_PAGES = dict(
    bootstrap=_bs,
    bootstrap2=_bs,
    bootstrap3=_bs,
    bootstrap3_3=_bs33,
    bootstrap4=_bs4,
    bootstrap5=_bs5,
    semantic=_se,
    foundation=_fa,
    bulma=_bulma,
    materialize=_materialize,
)

PREV_LABEL = "&laquo;"
NEXT_LABEL = "&raquo;"
RECORD_NAME = "records"

DISPLAY_MSG = "displaying <b>{start} - {end}</b> {record_name} in \
total <b>{total}</b>"

SEARCH_MSG = "found <b>{found}</b> {record_name}, \
displaying <b>{start} - {end}</b>"

_bs4 = '<nav aria-label="..."><ul class="pagination {0} {1}">'
_bs5 = '<nav aria-label="..."><ul class="pagination {0} {1}">'
_bs33 = '<nav aria-label="..."><ul class="pagination {0} {1}">'
_bulma = '<nav class="pagination {0} {1} {2}" role="navigation">\
{3}{4}<ul class="pagination-list">'
CSS_LINKS = dict(
    bootstrap='<div class="pagination {0} {1}"><ul>',
    bootstrap2='<div class="pagination {0} {1}"><ul>',
    bootstrap3='<ul class="pagination {0} {1}">',
    bootstrap3_3=_bs33,
    bootstrap4=_bs4,
    bootstrap5=_bs5,
    semantic='<div class="ui pagination menu">',
    foundation='<ul class="pagination {0} {1}">',
    bulma=_bulma,
    materialize='<ul class="pagination">',
)
CSS_LINKS_END = dict(
    bootstrap="</ul></div>",
    bootstrap2="</ul></div>",
    bootstrap3="</ul>",
    bootstrap3_3="</ul></nav>",
    bootstrap4="</ul></nav>",
    bootstrap5="</ul></nav>",
    semantic="</div>",
    foundation="</ul>",
    bulma="</ul></nav>",
    materialize="</ul>",
)

# foundation alignment
F_ALIGNMENT = '<div class="pagination-{0}">'


def get_parameter(param=None, args=None, default="page"):
    if not args:
        args = request.args.copy()
        args.update(request.view_args.copy())

    if not param:
        pk = "page_parameter" if default == "page" else "per_page_parameter"
        param = args.get(pk)
        if not param:
            param = current_app.config.get(pk.upper())

    return param or default


def get_page_parameter(param=None, args=None):
    return get_parameter(param, args, "page")


def get_per_page_parameter(param=None, args=None):
    return get_parameter(param, args, "per_page")


def get_page_args(
    page_parameter=None, per_page_parameter=None, for_test=False, **kwargs
):
    """param order: 1. passed parameter 2. request.args 3: config value
    for_test will return page_parameter and per_page_parameter"""
    args = request.args.copy()
    args.update(request.view_args.copy())

    page_name = get_page_parameter(page_parameter, args)
    per_page_name = get_per_page_parameter(per_page_parameter, args)
    for name in (page_name, per_page_name):
        if name in kwargs:
            args.setdefault(name, kwargs[name])

    if for_test:
        return page_name, per_page_name

    page = int(args.get(page_name, 1, type=int))
    per_page = args.get(per_page_name, type=int)
    if not per_page:
        per_page = int(current_app.config.get("PER_PAGE", 10))
    else:
        per_page = int(per_page)

    offset = (page - 1) * per_page
    return page, per_page, offset


def get_param_value(name, kwargs={}, default=None, cfg_name="", prefix="pagination"):
    """Get parameter value from kwargs or config"""
    config_name = cfg_name or name
    if prefix:
        config_name = "{}_{}".format(prefix, config_name)

    cfg_value = current_app.config.get(config_name.upper(), default)
    return kwargs.get(name, cfg_value)


class Pagination(object):
    """A simple pagination extension for flask."""

    def __init__(self, found=0, **kwargs):
        """Detail parameters.

            **found**: used when searching

            **page**: current page

            **per_page**: how many records displayed on one page

            **page_parameter**: a name(string) of a GET parameter that holds \
            a page index, Use it if you want to iterate over multiple \
            Pagination objects simultaneously.
            default is 'page'.

            **per_page_parameter**: a name for per_page likes page_parameter.
            default is 'per_page'.

            **inner_window**: how many links around current page

            **outer_window**: how many links near first/last link

            **prev_label**: text for previous page, default is **&laquo;**

            **next_label**: text for next page, default is **&raquo;**

            **search**: search or not?

            **total**: total records for pagination

            **display_msg**: text for pagination information

            **search_msg**: text for search information

            **record_name**: record name showed in pagination information

            **link_size**: font size of page links

            **alignment**: the alignment of pagination links

            **href**: Add custom href for links - this supports forms \
            with post method. It MUST contain {0} to format page number

            **show_single_page**: decide whether or not a single page \
            returns pagination

            **bs_version**: the version of bootstrap, default is **4**

            **css_framework**: the css framework, default is **bootstrap4**

            **anchor**: anchor parameter, appends to page href

            **format_total**: number format total, like **1,234**, \
            default is False

            **format_number**: number format start and end, like **1,234**, \
            default is False

            **url_coding**: coding for url encoding, default is **utf-8**

            **bulma_style**: page link style for bulma css framework

            **prev_rel**: rel of previous page

            **next_rel**: rel of next page

            **include_first_page_number**: include 1 for first page or not

        """
        self.found = found
        page_parameter = kwargs.get("page_parameter")
        if not page_parameter:
            page_parameter = get_page_parameter()

        self.page_parameter = page_parameter
        self.page = int(kwargs.get(self.page_parameter, 1))

        if self.page < 1:
            self.page = 1

        per_page_param = kwargs.get("per_page_parameter")
        if not per_page_param:
            per_page_param = get_per_page_parameter()

        self.per_page_parameter = per_page_param
        self.per_page = int(
            get_param_value(per_page_param, kwargs, 10, cfg_name="per_page", prefix="")
        )
        self.is_disabled = self.per_page < 1
        self.skip = (self.page - 1) * self.per_page
        self.inner_window = int(get_param_value("inner_window", kwargs, 2))
        self.outer_window = int(get_param_value("outer_window", kwargs, 1))
        self.prev_label = get_param_value("prev_label", kwargs, PREV_LABEL)
        self.next_label = get_param_value("next_label", kwargs, NEXT_LABEL)
        self.search = kwargs.get("search", False)
        self.total = kwargs.get("total", 0)
        self.format_total = get_param_value("format_total", kwargs, False)
        self.format_number = get_param_value("format_number", kwargs, False)
        self.url_coding = get_param_value("url_coding", kwargs, "utf-8")
        self.display_msg = get_param_value("display_msg", kwargs, DISPLAY_MSG)
        self.search_msg = get_param_value("search_msg", kwargs, SEARCH_MSG)
        self.record_name = get_param_value("record_name", kwargs, RECORD_NAME)
        self.css_framework = get_param_value(
            "css_framework", kwargs, "bootstrap4"
        ).lower()
        if self.css_framework not in CURRENT_PAGES:
            self.css_framework = "bootstrap4"

        if self.css_framework.startswith("bootstrap"):
            bs_version = self.css_framework[9:]
            if bs_version in ("3_3", "3.3"):
                self.bs_version = "3.3"
            elif bs_version:
                self.bs_version = bs_version
            else:
                self.bs_version = get_param_value("bs_version", kwargs, 4)
                if self.bs_version in (2, "2"):
                    self.css_framework = "bootstrap"
                elif self.bs_version in (3, "3"):
                    self.css_framework = "bootstrap3"
                elif self.bs_version in ("3.3", "3_3"):
                    self.css_framework = "bootstrap3_3"
                elif self.bs_version in (4, "4"):
                    self.css_framework = "bootstrap4"
                elif self.bs_version in (5, "5"):
                    self.css_framework = "bootstrap5"

            if not isinstance(self.bs_version, int):
                if self.bs_version.isdigit():
                    self.bs_version = int(self.bs_version)
                else:
                    self.bs_version = float(self.bs_version)

        self.link_size = get_param_value("link_size", kwargs, "")
        if self.link_size:
            if self.css_framework == "foundation":
                self.link_size = ""
            elif self.css_framework == "bulma":
                self.link_size = " is-{0}".format(self.link_size)
            else:
                self.link_size = " pagination-{0}".format(self.link_size)

        self.bulma_style = get_param_value("bulma_style", kwargs, "")
        if self.bulma_style:
            self.bulma_style = " is-{0}".format(self.bulma_style)

        self.prev_rel = get_param_value("prev_rel", kwargs, "")
        if self.prev_rel:
            self.prev_rel = ' rel="{}"'.format(self.prev_rel)

        self.next_rel = get_param_value("next_rel", kwargs, "")
        if self.next_rel:
            self.next_rel = ' rel="{}"'.format(self.next_rel)

        self.alignment = get_param_value("alignment", kwargs, "")
        if self.alignment and self.css_framework.startswith("bootstrap"):
            if self.css_framework in ("bootstrap4", "bootstrap5"):
                if self.alignment == "center":
                    self.alignment = " justify-content-center"
                elif self.alignment in ("right", "end"):
                    self.alignment = " justify-content-end"

            elif self.css_framework == "bootstrap2":
                self.alignment = " pagination-{0}".format(self.alignment)
            else:
                # v3 does not support this way
                # use this way: <div class="text-center/right">...</div>
                self.alignment = ""

        if self.alignment and self.css_framework == "bulma":
            self.alignment = " is-{0}".format(self.alignment)

        self.href = kwargs.get("href")
        self.anchor = kwargs.get("anchor")
        self.show_single_page = get_param_value("show_single_page", kwargs, False)

        self.link = LINK
        if self.css_framework == "bootstrap4":
            self.link = BS4_LINK
        elif self.css_framework == "bootstrap5":
            self.link = BS5_LINK
        elif self.css_framework == "semantic":
            self.link = SEMANTIC_LINK
        elif self.css_framework == "bulma":
            self.link = BULMA_LINK
        elif self.css_framework == "materialize":
            self.link = MATERIALIZE_LINK

        self.current_page_fmt = CURRENT_PAGES[self.css_framework]
        self.link_css_fmt = CSS_LINKS[self.css_framework]
        self.gap_marker_fmt = GAP_MARKERS[self.css_framework]
        self.prev_disabled_page_fmt = PREV_DISABLED_PAGES[self.css_framework]
        self.next_disabled_page_fmt = NEXT_DISABLED_PAGES[self.css_framework]
        self.prev_page_fmt = PREV_PAGES[self.css_framework]
        self.next_page_fmt = NEXT_PAGES[self.css_framework]
        self.css_end_fmt = CSS_LINKS_END[self.css_framework]
        self.include_first_page_number = get_param_value(
            "include_first_page_number", kwargs, False
        )
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
        if self.is_disabled:
            self.total_pages = 1
            self.has_prev = self.has_next = False
        else:
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
            page = self.page - 1
            if self.page <= 2 and not self.include_first_page_number:
                page = None

            url = self.page_href(page)
            if self.css_framework == "materialize":
                args = (url, self.prev_rel)
            else:
                args = (url, self.prev_label, self.prev_rel)

            return self.prev_page_fmt.format(*args)

        return self.prev_disabled_page_fmt.format(self.prev_label)

    @property
    def next_page(self):
        if self.has_next:
            url = self.page_href(self.page + 1)
            if self.css_framework == "materialize":
                args = (url, self.next_rel)
            else:
                args = (url, self.next_label, self.next_rel)

            return self.next_page_fmt.format(*args)

        return self.next_disabled_page_fmt.format(self.next_label)

    @property
    def first_page(self):
        # current page is first page
        if self.has_prev:
            if self.include_first_page_number:
                return self.link.format(self.page_href(1), 1)

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
        if self.css_framework == "foundation" and self.alignment:
            s.insert(0, F_ALIGNMENT.format(self.alignment))
            s.append("</div>")

        return Markup("".join(s))

    @property
    def links(self):
        """Get all the pagination links."""
        if self.total_pages <= 1:
            if self.show_single_page:
                return self._get_single_page_link()

            return ""

        if self.css_framework == "bulma":
            s = [
                self.link_css_fmt.format(
                    self.link_size,
                    self.alignment,
                    self.bulma_style,
                    self.prev_page,
                    self.next_page,
                )
            ]
            for page in self.pages:
                s.append(self.single_page(page) if page else self.gap_marker_fmt)

            s.append(self.css_end_fmt)
        else:
            s = [self.link_css_fmt.format(self.link_size, self.alignment)]
            s.append(self.prev_page)
            for page in self.pages:
                s.append(self.single_page(page) if page else self.gap_marker_fmt)

            s.append(self.next_page)
            s.append(self.css_end_fmt)
            if self.css_framework == "foundation" and self.alignment:
                s.insert(0, F_ALIGNMENT.format(self.alignment))
                s.append("</div>")

        return Markup("".join(s))

    @property
    def info(self):
        """Get the pagination information."""
        s = ['<div class="pagination-page-info">']
        page_msg = self.search_msg if self.search else self.display_msg
        if self.format_total:
            total_text = "{0:,}".format(self.total)
        else:
            total_text = "{0}".format(self.total)

        if self.is_disabled:
            start = 1
            end = self.found if self.search else self.total
        else:
            start = 1 + (self.page - 1) * self.per_page
            end = start + self.per_page - 1
            if end > self.total:
                end = self.found if self.search else self.total

            if start > self.total:
                start = self.found if self.search else self.total

        if self.format_number:
            start_text = "{0:,}".format(start)
            end_text = "{0:,}".format(end)
        else:
            start_text = start
            end_text = end

        s.append(
            page_msg.format(
                found=self.found,
                total=total_text,
                start=start_text,
                end=end_text,
                record_name=self.record_name,
            )
        )
        s.append("</div>")
        return Markup("".join(s))

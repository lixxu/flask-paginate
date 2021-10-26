"""Tests for flask-paginate."""
import unittest

import pytest
from flask import Flask
from flask_paginate import (
    BS4_LINK,
    CSS_LINKS,
    CSS_LINKS_END,
    CURRENT_PAGES,
    DISPLAY_MSG,
    GAP_MARKERS,
    NEXT_DISABLED_PAGES,
    NEXT_LABEL,
    NEXT_PAGES,
    PREV_DISABLED_PAGES,
    PREV_LABEL,
    PREV_PAGES,
    RECORD_NAME,
    SEARCH_MSG,
    Pagination,
    get_page_args
    )


class FlaskTestMixin(unittest.TestCase):
    """A mixin for a flask test."""

    def setUp(self):
        """Run the setUp for the app for the test."""
        self.app = Flask(__name__)

        def mocked_url_route():
            return "hello world"

        mocked_url_route.methods = ["GET"]

        self.app.add_url_rule("/", "test_route", mocked_url_route)
        self.app_client = self.app.test_client()


class TestGetPageArgs(FlaskTestMixin):
    """Tests for the get_page_args function."""

    def test_get_page_args_fails_outside_of_request_context(self):
        """get_page_args raises a RuntimeError if called with no request ctx.
        """
        with pytest.raises(RuntimeError):
            get_page_args()

    def test_get_page_args_works_inside_of_request_context(self):
        """get_page_args raises no error if called with a request ctx."""
        with self.app.test_request_context("/"):
            self.app.preprocess_request()
            get_page_args()
            page_param, per_page_param = get_page_args(
                page_parameter="p", for_test=True
            )
            assert page_param == "p"
            assert per_page_param == "per_page"

            page_param, per_page_param = get_page_args(
                per_page_parameter="pp", for_test=True
            )
            assert page_param == "page"
            assert per_page_param == "pp"


class TestPagination(FlaskTestMixin):
    """Tests for the Pagination class."""

    def test_defaults(self):
        """Test the default values of the kwargs."""
        with self.app.test_request_context("/"):
            pagination = Pagination()
            assert pagination.found == 0
            assert pagination.page_parameter == "page"
            assert pagination.per_page_parameter == "per_page"
            assert pagination.page == 1
            assert pagination.per_page == 10
            assert pagination.inner_window == 2
            assert pagination.outer_window == 1
            assert pagination.prev_label == PREV_LABEL
            assert pagination.next_label == NEXT_LABEL
            assert pagination.search is False
            assert pagination.total == 0
            assert pagination.format_total is False
            assert pagination.format_number is False
            assert pagination.display_msg == DISPLAY_MSG
            assert pagination.search_msg == SEARCH_MSG
            assert pagination.record_name == RECORD_NAME
            assert pagination.css_framework == "bootstrap4"
            assert pagination.bs_version == 4
            assert pagination.link_size == ""
            assert pagination.alignment == ""
            assert pagination.href is None
            assert pagination.anchor is None
            assert pagination.show_single_page is False
            assert pagination.link == BS4_LINK
            assert (
                pagination.current_page_fmt
                == CURRENT_PAGES[pagination.css_framework]
            )
            assert (
                pagination.link_css_fmt == CSS_LINKS[pagination.css_framework]
            )
            assert (
                pagination.gap_marker_fmt
                == GAP_MARKERS[pagination.css_framework]
            )
            assert (
                pagination.prev_disabled_page_fmt
                == PREV_DISABLED_PAGES[pagination.css_framework]
            )
            assert (
                pagination.next_disabled_page_fmt
                == NEXT_DISABLED_PAGES[pagination.css_framework]
            )
            assert (
                pagination.prev_page_fmt
                == PREV_PAGES[pagination.css_framework]
            )
            assert (
                pagination.next_page_fmt
                == NEXT_PAGES[pagination.css_framework]
            )
            assert (
                pagination.css_end_fmt
                == CSS_LINKS_END[pagination.css_framework]
            )

    def test_pages_first_page(self):
        """Test the pages property is correct on the first page."""
        with self.app.test_request_context("/"):
            pagination = Pagination(total=100, found=100)
            assert pagination.pages == [1, 2, 3, 4, 5, None, 9, 10]

    def test_pages_outer_window_0(self):
        """Test that pages property is correct with outer_window=0."""
        with self.app.test_request_context("/"):
            pagination = Pagination(
                total=100,
                found=100,
                search=True,
                outer_window=0,
                page=5,
                inner_window=1,
            )
            assert pagination.pages == [1, None, 4, 5, 6, None, 10]

    def test_customize_page_parameter(self):
        with self.app.test_request_context("/"):
            pagination = Pagination(page_parameter="p")
            assert pagination.page_parameter == "p"
            assert pagination.per_page_parameter == "per_page"

    def test_customize_per_page_parameter(self):
        with self.app.test_request_context("/"):
            pagination = Pagination(per_page_parameter="pp")
            assert pagination.page_parameter == "page"
            assert pagination.per_page_parameter == "pp"

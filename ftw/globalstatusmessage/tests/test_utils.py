from ftw.globalstatusmessage.utils import is_path_included
from unittest2 import TestCase


class TestIsPathIncluded(TestCase):

    def test_included(self):
        self.assert_inclusion(
            {'/foo': True},
            included=['/'],
            excluded=[])

    def test_excluded(self):
        self.assert_inclusion(
            {'/foo': False},
            included=[],
            excluded=['/'])

    def test_exclude_top_include_below(self):
        self.assert_inclusion(
            {'/plone/subsite': True,
             '/plone/subsite/page': True,
             '/plone/page': False},
            included=['/plone/subsite'],
            excluded=['/plone'])

    def test_nested_subsites(self):
        self.assert_inclusion(
            {'/plone': True,
             '/plone/page': True,
             '/plone/siteA': False,
             '/plone/siteA/page': False,
             '/plone/siteA/siteB': True,
             '/plone/siteA/siteB/page': True},

            included=['/plone',
                      '/plone/siteA/siteB'],
            excluded=['/plone/siteA'])

    def assert_inclusion(self, expectation, included, excluded):
        got = dict((path, is_path_included(path, included, excluded))
                   for path in expectation.keys())
        self.assertEquals(expectation, got)

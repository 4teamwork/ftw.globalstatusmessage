from ftw.globalstatusmessage import testing
from ftw.testbrowser import browsing
from ftw.testbrowser.pages import plone
from Products.CMFPlone.utils import getFSVersionTuple
from unittest2 import TestCase


class TestNotInstalled(TestCase):
    layer = testing.STATUSMESSAGE_ZCML_FUNCTIONAL

    @browsing
    def test_viewlet_should_not_break(self, browser):
        # When the package is not installed, the viewlet should
        # not break anything.

        browser.open()
        self.assertEquals('Plone site', plone.first_heading())
        if getFSVersionTuple() > (5, ):
            html_container = browser.css('#global_statusmessage').first
        else:
            html_container = browser.css('#portal-top').first
        self.assertNotIn(
            'error',
            html_container.text,
            'The viewlet should not be rendered, but it seems'
            ' to have been rendered with an error.')

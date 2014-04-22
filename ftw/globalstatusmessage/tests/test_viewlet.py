from ftw.globalstatusmessage import testing
from ftw.testbrowser import browsing
from ftw.testbrowser.pages import plone
from unittest2 import TestCase


class TestNotInstalled(TestCase):
    layer = testing.STATUSMESSAGE_ZCML_FUNCTIONAL

    @browsing
    def test_viewlet_should_not_break(self, browser):
        # When the package is not installed, the viewlet should
        # not break anything.

        browser.open()
        self.assertEquals('Plone site', plone.first_heading())
        self.assertNotIn(
            'error',
            browser.css('#portal-top').first.text,
            'The viewlet should not be rendered, but it seems'
            ' to have been rendered with an error.')

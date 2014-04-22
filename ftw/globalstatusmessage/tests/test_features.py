from ftw.globalstatusmessage.testing import STATUSMESSAGE_FUNCTIONAL
from ftw.testbrowser import browser
from ftw.testbrowser import browsing
from plone.app.testing import SITE_OWNER_NAME
from unittest2 import TestCase


def statusmessage():
    if not browser.css('#globalstatusmessage dl'):
        return None
    dl = browser.css('#globalstatusmessage dl').first
    return {'type': dl.classes[1],
            'title': dl.terms[0],
            'message': dl.definitions[0]}


class TestConfiguringStatusMessage(TestCase):
    layer = STATUSMESSAGE_FUNCTIONAL

    @browsing
    def test_no_viewlet_by_default(self, browser):
        browser.open()
        self.assertEquals(None, statusmessage(),
                          'Expected no default status message.')

    @browsing
    def test_info_status_message(self, browser):
        browser.login(SITE_OWNER_NAME).visit(
            view='global_statusmessage_config')
        browser.fill(
            {'Active': True,
             'Type': 'information',
             'Title': 'Maintenance',
             'Message': 'Scheduled maintenance 20PM-22PM'}).submit()

        self.assertEquals(
            {'type': 'information',
             'title': 'Maintenance',
             'message': 'Scheduled maintenance 20PM-22PM'},
            statusmessage())

    @browsing
    def test_error_status_message(self, browser):
        browser.login(SITE_OWNER_NAME).visit(
            view='global_statusmessage_config')
        browser.fill(
            {'Active': True,
             'Type': 'error',
             'Title': 'Outage',
             'Message': 'Some parts are not available'}).submit()

        self.assertEquals(
            {'type': 'error',
             'title': 'Outage',
             'message': 'Some parts are not available'},
            statusmessage())

    @browsing
    def test_disabling_status_message(self, browser):
        browser.login(SITE_OWNER_NAME).visit(
            view='global_statusmessage_config')
        browser.fill(
            {'Active': True,
             'Type': 'information',
             'Title': 'Maintenance',
             'Message': 'Scheduled maintenance 20PM-22PM'}).submit()
        self.assertTrue(statusmessage(),
                        'Expected a message to be configured.')

        browser.visit(view='global_statusmessage_config')
        browser.fill({'Active': False}).submit()
        self.assertFalse(statusmessage(),
                        'Expected message to be no longer visible.')

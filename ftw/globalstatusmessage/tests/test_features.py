from ftw.builder import Builder
from ftw.builder import create
from ftw.globalstatusmessage.testing import STATUSMESSAGE_FUNCTIONAL
from ftw.testbrowser import browser
from ftw.testbrowser import browsing
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from unittest2 import TestCase
import transaction


def statusmessage():
    if not browser.css('#globalstatusmessage dl'):
        return None
    dl = browser.css('#globalstatusmessage dl').first
    return {'type': dl.classes[1],
            'title': dl.terms[0],
            'message': dl.definitions[0]}


class TestConfiguringStatusMessage(TestCase):
    layer = STATUSMESSAGE_FUNCTIONAL

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

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

    @browsing
    def test_exclude_subsite(self, browser):
        subsite = create(Builder('folder')
                         .titled('The Subsite')
                         .providing(INavigationRoot))

        browser.login().visit(view='global_statusmessage_config')
        browser.fill(
            {'Active': True,
             'Type': 'information',
             'Title': 'Maintenance',
             'Message': 'Scheduled Maintenance',
             'Exclude sites': ['The Subsite']}).submit()


        browser.visit(self.portal)
        self.assertTrue(
            statusmessage(),
            'Status message should be visible on site root.')

        page_on_site_root = create(Builder('page'))
        browser.visit(page_on_site_root)
        self.assertTrue(
            statusmessage(),
            'Status message should be visible on pages within site root.')

        browser.visit(subsite)
        self.assertFalse(
            statusmessage(),
            'Status message should not be visible on subsite.')

        page_on_subsite = create(Builder('page').within(subsite))
        browser.visit(page_on_subsite)
        self.assertFalse(
            statusmessage(),
            'Status message should not be visible on pages within subsite.')

    @browsing
    def test_exclude_site_root(self, browser):
        subsite = create(Builder('folder')
                         .titled('The Subsite')
                         .providing(INavigationRoot))

        browser.login().visit(view='global_statusmessage_config')
        browser.fill(
            {'Active': True,
             'Type': 'information',
             'Title': 'Maintenance',
             'Message': 'Scheduled Maintenance',
             'Exclude sites': ['Plone site']}).submit()


        browser.visit(self.portal)
        self.assertFalse(
            statusmessage(),
            'Status message should not be visible on site root.')

        page_on_site_root = create(Builder('page'))
        browser.visit(page_on_site_root)
        self.assertFalse(
            statusmessage(),
            'Status message should not be visible on pages within site root.')

        browser.visit(subsite)
        self.assertTrue(
            statusmessage(),
            'Status message should be visible on subsite.')

        page_on_subsite = create(Builder('page').within(subsite))
        browser.visit(page_on_subsite)
        self.assertTrue(
            statusmessage(),
            'Status message should be visible on pages within subsite.')

from ftw.builder import Builder
from ftw.builder import create
from ftw.globalstatusmessage.config import IS_PLONE_5
from ftw.globalstatusmessage.testing import STATUSMESSAGE_FUNCTIONAL
from ftw.testbrowser import browser
from ftw.testbrowser import browsing
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import TEST_USER_ID
from unittest2 import skip
from unittest2 import TestCase
import re


def statusmessage():
    if not browser.css('#globalstatusmessage .portalMessage'):
        return None
    message = browser.css('#globalstatusmessage .portalMessage').first

    if IS_PLONE_5:
        # Plone 5: <div class="portalMessage information">
        #              <strong>Info</strong>
        #              Message
        #          </div>
        title = message.css('strong').first.text
        text = re.sub(r'^{} *'.format(re.escape(title)), '', message.text)
    else:
        # Plone 4: <dl class="portalMessage information">
        #              <dt>Info</dt>
        #              <dd>Message</dd>
        #          </dl>
        title = message.css('dt').first.text
        text = message.css('dd').first.text

    type_ = message.classes[1]
    return {'type': type_,
            'title': title,
            'message': text}


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
                         .titled(u'The Subsite')
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
                         .titled(u'The Subsite')
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

    @browsing
    def test_disable_for_anonymous(self, browser):
        subsite = create(Builder('folder')
                         .titled(u'The Subsite')
                         .providing(INavigationRoot))

        browser.login().visit(view='global_statusmessage_config')
        browser.fill(
            {'Active': True,
             'Type': 'information',
             'Title': 'Maintenance',
             'Message': 'Scheduled Maintenance'}).submit()

        browser.logout().visit(self.portal)
        self.assertTrue(
            statusmessage(),
            'Status should be visible for anonymous by default.')

        browser.login().visit(view='global_statusmessage_config')
        browser.fill(
            {'Show to anonymous users?': False}).submit()

        browser.visit(self.portal)
        self.assertTrue(
            statusmessage(),
            'Status should still visible for logged in users.')

        browser.logout().reload()
        self.assertFalse(
            statusmessage(),
            'Status should no longer be visible for anonymous in users.')

    @skip('Await bugfix for #2947 in Products.CMFPlone')
    @browsing
    def test_global_status_message_not_duplicated(self, browser):
        """ Test we have only 1 global status message in the control panel """
        browser.login(SITE_OWNER_NAME).open(view='@@global_statusmessage_config')
        browser.fill(
            {'Active': True,
             'Type': 'information',
             'Title': 'Maintenance',
             'Message': 'Scheduled Maintenance'}).submit()

        browser.visit(view='@@global_statusmessage_config')
        self.assertEqual(1, len(browser.css('#globalstatusmessage')),
                         'Duplicate globalstatusmessage in gsm config')

        browser.visit(view='@@mail-controlpanel')
        self.assertEqual(1, len(browser.css('#globalstatusmessage')),
                         'Duplicate globalstatusmessage in mail config')

# -*- coding: utf-8 -*-
from copy import deepcopy
from ftw.builder import Builder
from ftw.builder import create
from ftw.globalstatusmessage.config import PROJECTNAME
from ftw.globalstatusmessage.interfaces import IStatusMessageConfigForm
from ftw.globalstatusmessage.testing import STATUSMESSAGE_FUNCTIONAL
from ftw.globalstatusmessage.tests import FunctionalTestCase
from ftw.globalstatusmessage.tests.helpers import view_registered
from ftw.publisher.core.communication import createResponse
from ftw.publisher.core.states import SuccessState
from ftw.publisher.core.utils import decode_for_json
from ftw.publisher.core.utils import encode_after_json
from ftw.publisher.sender.interfaces import IConfig
from ftw.publisher.sender.persistence import Realm
from ftw.testbrowser import browsing
from ftw.testbrowser.pages.statusmessages import info_messages
from plone import api
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.testing import logout, SITE_OWNER_NAME, SITE_OWNER_PASSWORD
from plone.registry.interfaces import IRegistry
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.Five import BrowserView
from zope.component import getMultiAdapter, getUtility
from zope.interface import Interface
from zope.schema import getFieldNames
import json
import transaction
import unittest2 as unittest


class ControlPanelTestCase(unittest.TestCase):

    layer = STATUSMESSAGE_FUNCTIONAL

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.controlpanel = self.portal['portal_controlpanel']

    def test_controlpanel_has_view(self):
        view = getMultiAdapter(
            (self.portal, self.request), name='global_statusmessage_config')
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_controlpanel_view_is_protected(self):
        from AccessControl import Unauthorized
        logout()
        with self.assertRaises(Unauthorized):
            self.portal.restrictedTraverse('@@global_statusmessage_config')

    def test_controlpanel_installed(self):
        actions = [a.getAction(self)['id']
                   for a in self.controlpanel.listActions()]
        self.assertIn('globalstatusmessage', actions)

    def test_controlpanel_removed_on_uninstall(self):
        qi = self.portal['portal_quickinstaller']
        qi.uninstallProducts(products=[PROJECTNAME])
        actions = [a.getAction(self)['id']
                   for a in self.controlpanel.listActions()]
        self.assertNotIn('globalstatusmessage', actions)


class PublishedControlPanelTestCase(FunctionalTestCase):

    enabled_bool = True
    enabled_anonymous_bool = True
    type_choice = u'information'
    title_textfield = u'Hello World'
    message_textfield = u'This is the message to the world'
    exclude_sites = None

    form_data = {
        'Active': enabled_bool,
        'Show to anonymous users?': enabled_anonymous_bool,
        'Type': type_choice,
        'Title': title_textfield,
        'Message': message_textfield,
    }

    expected_settings = {
        'enabled_bool': enabled_bool,
        'enabled_anonymous_bool': enabled_anonymous_bool,
        'type_choice': type_choice,
        'title_textfield': title_textfield,
        'message_textfield': message_textfield,
        'exclude_sites': None,
    }

    payload = json.dumps(decode_for_json(expected_settings))

    def setUp(self):
        super(PublishedControlPanelTestCase, self).setUp()
        self.grant('Manager')
        api.portal.get_tool('portal_setup').runAllImportStepsFromProfile(
            'profile-ftw.publisher.sender:default',
            ignore_dependencies=True
        )

    def test_all_settings_are_tested(self):
        """
        This test will fail if new settings are added to "IStatusMessageConfigForm"
        without having been added in this test case.
        """
        self.assertEqual(
            set(self.expected_settings.keys()),
            set(getFieldNames(IStatusMessageConfigForm)),
            msg='Have you added some fields to "IStatusMessageConfigForm" without updating the test case?'
        )

    @browsing
    def test_sender(self, browser):
        intercepted_data = {}

        class MockedReceiverView(BrowserView):
            def __call__(self):
                intercepted_data['jsondata'] = self.request.form.get('jsondata')
                return createResponse(SuccessState())

        config = IConfig(self.portal)
        config.appendRealm(Realm(1, self.portal.absolute_url(), SITE_OWNER_NAME, SITE_OWNER_PASSWORD))
        transaction.commit()

        with view_registered(MockedReceiverView, 'global_statusmessage_config_receiver',
                             required=(IPloneSiteRoot, Interface)):
            browser.login(SITE_OWNER_NAME).open(view='@@global_statusmessage_config')
            browser.fill(self.form_data)
            browser.click_on('Save and publish')

        self.assertDictEqual(
            self.expected_settings,
            encode_after_json(json.loads(intercepted_data['jsondata']))
        )

        self.assertEqual(
            ['Changes saved and published.'],
            info_messages()
        )

    @browsing
    def test_receiver(self, browser):
        browser.login().open(
            self.portal,
            view='@@global_statusmessage_config_receiver',
            data={'jsondata': self.payload},
            send_authenticator=True)

        registry = getUtility(IRegistry)
        settings = registry.forInterface(IStatusMessageConfigForm, check=False)

        self.assertDictEqual(
            {
                field_name: getattr(settings, field_name)
                for field_name in getFieldNames(IStatusMessageConfigForm)
            },
            self.expected_settings
        )

    @browsing
    def test_receiver_filters_not_existing_paths_before_setting_them(self, browser):
        subsite = create(Builder('folder')
                         .titled(u'subsite')
                         .providing(INavigationRoot))
        subsite_path = '/'.join(subsite.getPhysicalPath())

        settings = deepcopy(self.expected_settings)
        settings['exclude_sites'] = [subsite_path, '/not/existing']
        payload = json.dumps(decode_for_json(settings))

        browser.login().open(
            self.portal,
            view='@@global_statusmessage_config_receiver',
            data={'jsondata': payload},
            send_authenticator=True)

        registry = getUtility(IRegistry)
        store = registry.forInterface(IStatusMessageConfigForm, check=False)

        settings['exclude_sites'].remove('/not/existing')
        self.assertDictEqual(
            {
                field_name: getattr(store, field_name)
                for field_name in getFieldNames(IStatusMessageConfigForm)
            },
            settings
        )

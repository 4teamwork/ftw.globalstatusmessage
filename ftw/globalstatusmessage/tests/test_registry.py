# -*- coding: utf-8 -*-
from ftw.globalstatusmessage.config import PROJECTNAME
from ftw.globalstatusmessage.interfaces import IStatusMessageConfigForm
from ftw.globalstatusmessage.testing import STATUSMESSAGE_FUNCTIONAL
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import unittest2 as unittest


class RegistryTestCase(unittest.TestCase):

    layer = STATUSMESSAGE_FUNCTIONAL

    def setUp(self):
        self.portal = self.layer['portal']
        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(IStatusMessageConfigForm)

    def test_enabled_bool_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'enabled_bool'))
        self.assertFalse(self.settings.enabled_bool)

    def test_enabled_anonymous_bool_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'enabled_anonymous_bool'))
        self.assertTrue(self.settings.enabled_anonymous_bool)

    def test_type_choice_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'type_choice'))
        self.assertIsNone(self.settings.type_choice)

    def test_title_textfield_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'title_textfield'))
        self.assertIsNone(self.settings.title_textfield)

    def test_message_textfield_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'message_textfield'))
        self.assertIsNone(self.settings.message_textfield)

    def test_records_removed_on_uninstall(self):
        qi = self.portal['portal_quickinstaller']
        qi.uninstallProducts(products=[PROJECTNAME])

        BASE_REGISTRY = 'ftw.globalstatusmessage.interfaces.IStatusMessageConfigForm.'
        records = [
            BASE_REGISTRY + 'enabled_bool',
            BASE_REGISTRY + 'enabled_anonymous_bool',
            BASE_REGISTRY + 'type_choice',
            BASE_REGISTRY + 'title_textfield',
            BASE_REGISTRY + 'message_textfield',
        ]

        for r in records:
            self.assertNotIn(r, self.registry)

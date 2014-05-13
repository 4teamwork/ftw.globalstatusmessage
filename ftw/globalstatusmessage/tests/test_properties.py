# -*- coding: utf-8 -*-
from ftw.globalstatusmessage.testing import STATUSMESSAGE_FUNCTIONAL

import unittest2 as unittest

PROJECTNAME = 'ftw.globalstatusmessage'


class PropertiesTestCase(unittest.TestCase):

    layer = STATUSMESSAGE_FUNCTIONAL

    def setUp(self):
        self.portal = self.layer['portal']
        self.properties = self.portal['portal_properties']

    def test_ftw_globalstatusmessage_properties(self):
        self.assertIn('ftw_globalstatusmessage_properties', self.properties)

    def test_enabled_property(self):
        gsm_properties = self.properties.ftw_globalstatusmessage_properties
        self.assertTrue(gsm_properties.hasProperty('Active'))
        self.assertEqual(gsm_properties.getPropertyType('Active'), 'boolean')

    def test_type_property(self):
        gsm_properties = self.properties.ftw_globalstatusmessage_properties
        self.assertTrue(gsm_properties.hasProperty('Type'))
        self.assertEqual(gsm_properties.getPropertyType('Type'), 'string')

    def test_title_property(self):
        gsm_properties = self.properties.ftw_globalstatusmessage_properties
        self.assertTrue(gsm_properties.hasProperty('Title'))
        self.assertEqual(gsm_properties.getPropertyType('Title'), 'string')

    def test_message_property(self):
        gsm_properties = self.properties.ftw_globalstatusmessage_properties
        self.assertTrue(gsm_properties.hasProperty('Message'))
        self.assertEqual(gsm_properties.getPropertyType('Message'), 'string')

    def test_properties_removed_on_uninstall(self):
        qi = self.portal['portal_quickinstaller']
        qi.uninstallProducts(products=[PROJECTNAME])
        self.assertNotIn(
            'ftw_globalstatusmessage_properties', self.properties)

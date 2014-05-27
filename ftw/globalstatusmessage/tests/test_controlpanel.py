# -*- coding: utf-8 -*-
from ftw.globalstatusmessage.config import PROJECTNAME
from ftw.globalstatusmessage.testing import STATUSMESSAGE_FUNCTIONAL
from plone.app.testing import logout
from zope.component import getMultiAdapter

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

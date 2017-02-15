# -*- coding: utf-8 -*-
from ftw.globalstatusmessage.config import PROJECTNAME
from ftw.globalstatusmessage.interfaces import IStatusMessageConfigForm
from ftw.globalstatusmessage.testing import STATUSMESSAGE_FUNCTIONAL
from plone import api
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import unittest2 as unittest


class UpgradeTestCaseBase(unittest.TestCase):

    layer = STATUSMESSAGE_FUNCTIONAL

    def setUp(self, from_version, to_version):
        self.portal = self.layer['portal']
        self.setup = self.portal['portal_setup']
        self.profile_id = u'ftw.globalstatusmessage:default'
        self.from_version = from_version
        self.to_version = to_version

    def _get_upgrade_step(self, title):
        self.setup.setLastVersionForProfile(self.profile_id, self.from_version)
        upgrades = self.setup.listUpgrades(self.profile_id)
        steps = []
        for s in upgrades:
            try:
                if s['title'] == title:  # handle single upgrade steps
                    steps.append(s)
            except TypeError:
                if s[0]['title'] == title:  # handle lists of upgrade steps
                    steps.append(s[0])

        assert len(steps) == 1
        return steps[0]

    def _do_upgrade_step(self, step):
        request = self.layer['request']
        request.form['profile_id'] = self.profile_id
        request.form['upgrades'] = [step['id']]
        self.setup.manage_doUpgrades(request=request)

    def _how_many_upgrades_to_do(self):
        self.setup.setLastVersionForProfile(self.profile_id, self.from_version)
        upgrades = self.setup.listUpgrades(self.profile_id)
        assert len(upgrades) > 0
        return len(upgrades)


class Upgrade1003to1004TestCase(UpgradeTestCaseBase):

    def setUp(self):
        UpgradeTestCaseBase.setUp(self, u'1003', u'1004')

    def test_upgrade_step_registrations(self):
        version = self.setup.getLastVersionForProfile(self.profile_id)[0]
        self.assertTrue(version >= self.to_version)
        self.assertGreaterEqual(self._how_many_upgrades_to_do(), 1)

    def test_upgrade_step(self):
        title = u'Migrate configlet to plone.app.registry'
        step = self._get_upgrade_step(title)
        self.assertIsNotNone(step)

        # simulate state on previous profile version
        pprops = self.portal['portal_properties']
        # add ftw_globalstatusmessage_properties property sheet
        pprops.addPropertySheet('ftw_globalstatusmessage_properties')
        self.assertIn('ftw_globalstatusmessage_properties', pprops)
        # remove registry records
        uninstall = 'profile-{0}:uninstall'.format(PROJECTNAME)
        setup = api.portal.get_tool('portal_setup')
        setup.runImportStepFromProfile(uninstall, 'plone.app.registry')
        registry = getUtility(IRegistry)
        with self.assertRaises(KeyError):
            registry.forInterface(IStatusMessageConfigForm)

        # run the upgrade step to validate the update
        self._do_upgrade_step(step)

        self.assertNotIn('ftw_globalstatusmessage_properties', pprops)
        fields = [
            'enabled_bool',
            'type_choice',
            'title_textfield',
            'message_textfield',
        ]
        settings = registry.forInterface(IStatusMessageConfigForm)
        for f in fields:
            self.assertTrue(hasattr(settings, f))


class Upgrade1400to1500TestCase(UpgradeTestCaseBase):

    def setUp(self):
        UpgradeTestCaseBase.setUp(self, u'1400', u'1500')

    def test_upgrade_step_registrations(self):
        version = self.setup.getLastVersionForProfile(self.profile_id)[0]
        self.assertGreaterEqual(version, self.to_version)
        self.assertGreaterEqual(self._how_many_upgrades_to_do(), 1)

    def test_upgrade_registry(self):
        title = u'Update registry: enable new configuration enabled_anonymous'
        step = self._get_upgrade_step(title)
        self.assertIsNotNone(step)

        from plone.registry.interfaces import IRegistry
        from zope.component import getUtility
        registry = getUtility(IRegistry)

        # simulate state on previous version
        record = IStatusMessageConfigForm.__identifier__ + '.enabled_anonymous_bool'
        del registry.records[record]

        with self.assertRaises(KeyError):
            registry.forInterface(IStatusMessageConfigForm)

        # execute upgrade step and verify changes were applied
        self._do_upgrade_step(step)
        settings = registry.forInterface(IStatusMessageConfigForm)
        self.assertTrue(hasattr(settings, 'enabled_anonymous_bool'))
        self.assertEqual(settings.enabled_anonymous_bool, True)

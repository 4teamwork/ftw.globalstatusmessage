# -*- coding: utf-8 -*-
from ftw.globalstatusmessage.config import PROJECTNAME
from ftw.globalstatusmessage.interfaces import IStatusMessageConfigForm
from ftw.upgrade import UpgradeStep
from plone import api
from plone.registry.interfaces import IRegistry
from Products.CMFPlone.utils import safe_unicode
from zope.component import getUtility

import logging

LOG = logging.getLogger('ftw.globalstatusmessage.upgrades:1004')


class MigrateConfiglet(UpgradeStep):

    def __call__(self):
        # remove property sheet
        pprops = api.portal.get_tool('portal_properties')
        if 'ftw_globalstatusmessage_properties' in pprops:
            gsm_props = pprops.ftw_globalstatusmessage_properties
            del pprops['ftw_globalstatusmessage_properties']
        else:
            gsm_props = None

        # add registry records
        default = 'profile-{0}:default'.format(PROJECTNAME)
        setup = api.portal.get_tool('portal_setup')
        setup.runImportStepFromProfile(default, 'plone.app.registry')
        registry = getUtility(IRegistry)
        r = registry.forInterface(IStatusMessageConfigForm)

        # migrate current values
        if gsm_props is not None:
            r.enabled_bool = gsm_props.getProperty('Active', r.enabled_bool)
            r.type_choice = safe_unicode(
                gsm_props.getProperty('Type', r.type_choice))
            r.title_textfield = safe_unicode(
                gsm_props.getProperty('Title', r.title_textfield))
            r.message_textfield = safe_unicode(
                gsm_props.getProperty('Message', r.message_textfield))

        LOG.info('Configlet was migrated to plone.app.registry.')

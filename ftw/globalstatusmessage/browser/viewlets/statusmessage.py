# -*- coding: utf-8 -*-
from ftw.globalstatusmessage.interfaces import IStatusMessageConfigForm
from plone.app.layout.viewlets import common
from plone.registry.interfaces import IRegistry
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getUtility


class StatusmessageViewlet(common.PathBarViewlet):
    index = ViewPageTemplateFile('statusmessage.pt')

    def update(self):
        super(StatusmessageViewlet, self).update()
        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(IStatusMessageConfigForm)

    def settings(self):
        return self.settings

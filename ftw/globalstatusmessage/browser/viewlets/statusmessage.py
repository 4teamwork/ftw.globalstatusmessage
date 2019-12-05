# -*- coding: utf-8 -*-
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from ftw.globalstatusmessage.config import IS_PLONE_5
from ftw.globalstatusmessage.interfaces import IStatusMessageConfigForm
from ftw.globalstatusmessage.utils import is_path_included
from plone import api
from plone.app.layout.viewlets import common
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory


class StatusmessageViewlet(common.PathBarViewlet):
    index = ViewPageTemplateFile('statusmessage.pt')
    is_plone_5 = IS_PLONE_5

    def update(self):
        super(StatusmessageViewlet, self).update()

    def render(self):
        registry = getUtility(IRegistry)
        self.settings = registry.forInterface(IStatusMessageConfigForm)

        if not self.settings.enabled_bool:
            return ''

        if api.user.is_anonymous() and not self.settings.enabled_anonymous_bool:
            return ''

        if not self.show_in_current_context():
            return ''

        return self.index()

    def show_in_current_context(self):
        excluded_site_paths = self.settings.exclude_sites or []
        if not excluded_site_paths:
            return True

        included_site_paths = set(self._all_sites_paths()) \
                              - set(excluded_site_paths)
        return is_path_included('/'.join(self.context.getPhysicalPath()),
                                included_site_paths,
                                excluded_site_paths)

    def _all_sites_paths(self):
        vocabulary_factory = getUtility(
            IVocabularyFactory,
            name='ftw.globalstatusmessage:sites_vocabulary')
        return [term.value for term in vocabulary_factory(None)]

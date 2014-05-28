# -*- coding: utf-8 -*-
from ftw.globalstatusmessage import _
from ftw.globalstatusmessage.interfaces import IStatusMessageConfigForm
from plone.app.registry.browser import controlpanel


class StatusMessageEditForm(controlpanel.RegistryEditForm):
    schema = IStatusMessageConfigForm
    label = _(u'Global Status Message')
    description = _(u'Settings for Global Status Message.')


class StatusMessageControlPanel(controlpanel.ControlPanelFormWrapper):
    form = StatusMessageEditForm

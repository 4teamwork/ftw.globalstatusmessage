# -*- coding: utf-8 -*-
from Acquisition._Acquisition import aq_inner
from ftw.globalstatusmessage import _
from ftw.globalstatusmessage.interfaces import IStatusMessageConfigForm
from ftw.globalstatusmessage.utils import is_profile_installed
from plone import api
from plone.app.registry.browser import controlpanel
from plone.registry.interfaces import IRegistry
from Products.statusmessages import STATUSMESSAGEKEY
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import button
from zope.annotation import IAnnotations
from zope.component import getUtility
from zope.i18nmessageid import MessageFactory
from zope.schema import getFieldNames
import json
import pkg_resources

try:
    pkg_resources.get_distribution('ftw.publisher.sender')
except pkg_resources.DistributionNotFound:
    pass
else:
    from ftw.publisher.sender.interfaces import IConfig
    from ftw.publisher.sender.utils import sendJsonToRealm
    from ftw.publisher.core.utils import decode_for_json


plone_messagefactory = MessageFactory("plone")


class StatusMessageEditForm(controlpanel.RegistryEditForm):
    schema = IStatusMessageConfigForm
    label = _(u'Global Status Message')
    description = _(u'Settings for Global Status Message.')


class PublishingStatusMessageEditForm(StatusMessageEditForm):
    """
    A special edit form which handles the publishing of the global status message
    to a "ftw.publisher.receiver" instance.

    Please note that the buttons are rendered in the order as they are defined.
    """

    @button.buttonAndHandler(plone_messagefactory(u"Save"), name='save')
    def handleSave(self, action):
        # Redeclare the save button because it is not inherited from the parent class.
        super(PublishingStatusMessageEditForm, self).handleSave(self, action)

    @button.buttonAndHandler(_(u'Save and publish'), name='save_and_publish')
    def handleSaveAndPublish(self, action):
        """
        The additional button to send to a "ftw.publisher.receiver" instance.
        """
        self.handleSave(self, action)

        self.send_to_receiver()

        # Consume Plone messages set by `handleSave` so we can set our own message.
        messages = IStatusMessage(self.request)
        if messages.show():
            self.request.response.cookies.pop(STATUSMESSAGEKEY)
            IAnnotations(self.request)[STATUSMESSAGEKEY] = None

        # Set a new Plone message.
        api.portal.show_message(
            message=_(u'Changes saved and published.'),
            request=self.request,
            type='info'
        )

    def updateActions(self):
        super(PublishingStatusMessageEditForm, self).updateActions()
        self.actions['save_and_publish'].addClass("context")

    @button.buttonAndHandler(plone_messagefactory(u'Cancel'), name='cancel')
    def handleCancel(self, action):
        # Redeclare the cancel button because it is not inherited from the parent class.
        super(PublishingStatusMessageEditForm, self).handleCancel(self, action)

    def send_to_receiver(self):
        data = json.dumps(
            decode_for_json(self.get_settings_data())
        )

        realms = IConfig(api.portal.get()).getRealms()
        for realm in realms:
            sendJsonToRealm(
                data,
                realm,
                'global_statusmessage_config_receiver'
            )

    def get_settings_data(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IStatusMessageConfigForm, check=False)

        data = {
            field_name: getattr(settings, field_name)
            for field_name in getFieldNames(IStatusMessageConfigForm)
        }

        return data


class StatusMessageControlPanel(controlpanel.ControlPanelFormWrapper):
    form = StatusMessageEditForm

    def __init__(self, context, request):
        super(StatusMessageControlPanel, self).__init__(context, request)

        if is_profile_installed('profile-ftw.publisher.sender:default'):
            self.form_instance = PublishingStatusMessageEditForm(
                aq_inner(context), request
            )
            self.form_instance.__name__ = self.__name__

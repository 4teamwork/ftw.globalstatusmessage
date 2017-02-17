# -*- coding: utf-8 -*-
from ftw.globalstatusmessage import _
from plone.supermodel import model
from zope import schema
from zope.interface import Interface


class IStatusMessageConfigForm(model.Schema):
    """This interface defines the configlet."""

    enabled_bool = schema.Bool(
        title=_(u"statusmessage_label_Active", default=u"Active"),
        required=False)

    enabled_anonymous_bool = schema.Bool(
        title=_(u"statusmessage_label_anonymous", default=u"Show to anonymous users?"),
        default=True,  # for backward compatibility
        required=False)

    type_choice = schema.Choice(
        title=_(u"statusmessage_label_type", default=u"Type"),
        values=[_(u"information"),
                _(u"warning"),
                _(u"error")],
        required=False)

    title_textfield = schema.TextLine(
        title=_(u"statusmessage_label_title", default=u"Title"),
        required=False)

    message_textfield = schema.Text(
        title=_(u"statusmessage_label_message", default=u"Message"),
        required=False)

    exclude_sites = schema.List(
        title=_(u'statusmessage_label_exclude_sites',
                default=u'Exclude sites'),
        description=_(u'statusmessage_help_exclude_sites',
                      default=u'The message will not be shown on any content'
                      u' within containers which are selected here.'
                      u' If however a container is selected but a selectable'
                      u' sub container is not selected, contents within the'
                      u' the sub container will display the message.'),
        required=False,
        value_type=schema.Choice(
            vocabulary='ftw.globalstatusmessage:sites_vocabulary'))


class IGlobalStatusMessageLayer(Interface):
    """ftw.globalstatusmessage browser layer.
    """

from zope.interface import Interface
from zope import schema
from ftw.globalstatusmessage import _
from plone.theme.interfaces import IDefaultPloneLayer


class IStatusMessageConfigForm(Interface):
    """This interface defines the configlet."""
    enabled_bool = schema.Bool(
    title = _(u"statusmessage_label_Active", default=u"Active"),
    required = False)
    type_choice = schema.Choice(
    title = _(u"statusmessage_label_type", default=u"Type"),
    values = [_(u"information"),
    _(u"warning"),
    _(u"error")],
    required = False)
    title_textfield = schema.TextLine(
    title = _(u"statusmessage_label_title", default= u"Title"),
    required = False)
    message_textfield = schema.Text(
    title = _(u"statusmessage_label_message", default= u"Message"),
    required = False)


class IGlobalStatusMessageLayer(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer.
    """

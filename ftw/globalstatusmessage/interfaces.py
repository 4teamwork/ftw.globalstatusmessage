from zope.interface import Interface
from zope import schema
from ftw.globalstatusmessage import _


class IStatusMessageConfigForm(Interface):
    """This interface defines the configlet."""
    enabled_bool = schema.Bool(title = _(u"Active"), required = False)
    type_choice = schema.Choice(title = _(u"Type"), values = [_(u"information"), _(u"Warning"), _(u"Error")], required = False)
    message_textfield = schema.Text(title = _(u"Message"), required = False)

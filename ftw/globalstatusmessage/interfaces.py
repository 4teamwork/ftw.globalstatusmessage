from zope.interface import Interface
from zope import schema
from globalstatusmessage import _
class iglobalstatusmessage(interface):

    message_textfield = schema.TextLine(title = _(u"Message"),required = false)
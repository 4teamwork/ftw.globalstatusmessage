from zope.formlib import form
from globalstatusmessage import _
from Products.Five.formlib import formbase
from interfaces import iglobalstatusmessage


class MessageForm(formbase.EditFormBase):
    form_fields = form.Fields(message_textfield)

    label = _(u"Global Statusmessage")

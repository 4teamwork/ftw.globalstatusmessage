from zope.formlib import form
from Products.Five.formlib import formbase
from ftw.globalstatusmessage.interfaces import IStatusMessageConfigForm
from ftw.globalstatusmessage import _
from plone.app.form.widgets.wysiwygwidget import WYSIWYGWidget


class MessageForm(formbase.EditFormBase):
    """This class defines the form"""
    form_fields = form.Fields(IStatusMessageConfigForm)
    form_fields['message_textfield'].custom_widget = WYSIWYGWidget

    label = _(u"Global Statusmessage")

from z3c.form import form, field
from plone.z3cform.layout import wrap_form
from ftw.globalstatusmessage.interfaces import IStatusMessageConfigForm
from ftw.globalstatusmessage import _
from plone.app.form.widgets.wysiwygwidget import WYSIWYGWidget


class GlobalStatusMessageForm(form.EditForm):
    """This class defines the form"""
    schema = IStatusMessageConfigForm
    fields = field.Fields(IStatusMessageConfigForm)
    fields['message_textfield'].custom_widget = WYSIWYGWidget

    label = _(u"Global Statusmessage")


GlobalStatusMessageView = wrap_form(GlobalStatusMessageForm)

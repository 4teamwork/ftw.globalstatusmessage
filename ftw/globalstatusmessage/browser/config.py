from ftw.globalstatusmessage import _
from ftw.globalstatusmessage.interfaces import IStatusMessageConfigForm
from plone.z3cform.layout import wrap_form
from z3c.form import form, field


class GlobalStatusMessageForm(form.EditForm):
    """This class defines the form"""
    schema = IStatusMessageConfigForm
    fields = field.Fields(IStatusMessageConfigForm)

    label = _(u"Global Statusmessage")


GlobalStatusMessageView = wrap_form(GlobalStatusMessageForm)

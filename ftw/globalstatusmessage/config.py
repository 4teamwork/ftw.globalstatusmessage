from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import IPloneSiteRoot
from ftw.globalstatusmessage.interfaces import IStatusMessageConfigForm
from zope.component import adapts
from zope.interface import implements


class FormAdapter(object):
    """This adapter acts as propagating storage for the z3c edit form,
    which does something like
    IStatusMessageConfigForm(self.context).message = '...'
    """
    implements(IStatusMessageConfigForm)
    adapts(IPloneSiteRoot)

    def __init__(self, context):
        pprop = getToolByName(context, 'portal_properties')
        self.statusProps = pprop.ftw_globalstatusmessage_properties

    def get_active(self):
        return self.statusProps.getProperty('Active')

    def set_active(self, value):
        self.statusProps._updateProperty('Active', value)

    enabled_bool = property(get_active, set_active)

    def get_type(self):
        return self.statusProps.getProperty('Type')

    def set_type(self, value):
        self.statusProps._updateProperty('Type', value)
    type_choice = property(get_type, set_type)

    def get_title(self):
        return self.statusProps.getProperty('Title')

    def set_title(self, value):
        self.statusProps._updateProperty('Title', value)

    title_textfield = property(get_title, set_title)

    def get_message(self):
        return self.statusProps.getProperty('Message').decode('utf-8')

    def set_message(self, value):

        if not value:
            value = ""

        self.statusProps._updateProperty('Message', value.encode('utf-8'))
    message_textfield = property(get_message, set_message)

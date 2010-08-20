from zope.interface import implements
from interfaces import IStatusMessageConfigForm
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFCore.utils import getToolByName
from zope.component import adapts
import Products


class FormAdapter(SchemaAdapterBase):
    implements(IStatusMessageConfigForm)
    adapts(Products.CMFPlone.Portal.PloneSite)

    def __init__(self, context):
        super(FormAdapter, self).__init__(context)
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

    def get_message(self):
        return self.statusProps.getProperty('Message')

    def set_message(self, value):
        self.statusProps._updateProperty('Message', value)
    message_textfield = property(get_message, set_message)

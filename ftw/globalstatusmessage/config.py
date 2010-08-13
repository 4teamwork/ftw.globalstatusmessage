from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from interfaces import iglobalstatusmessage
from OFS.SimpleItem import SimpleItem
from zope.component import getUtility
class globalstatusmessage(SimpleItem):
    implements(iglobalstatusmessage)
    
    message_text = FieldProperty(iglobalstatusmessage['message_textfield'])

    def form_adapter(context):
        return getUtility(Iglobalstatusmessage, name='Global_Statusmessage', context=context)
    
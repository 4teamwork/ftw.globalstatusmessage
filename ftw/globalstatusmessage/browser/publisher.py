from ftw.globalstatusmessage.interfaces import IStatusMessageConfigForm
from ftw.publisher.core import states
from ftw.publisher.core.communication import createResponse
from ftw.publisher.core.utils import encode_after_json
from plone.registry.interfaces import IRegistry
from Products.Five import BrowserView
from zope.component import getUtility
from zope.schema import getFieldNames
import json


class ConfigReceiverView(BrowserView):

    def __call__(self):
        data = encode_after_json(
            json.loads(self.request.form.get('jsondata'))
        )

        if not data:
            return createResponse(states.InvalidRequestError())

        registry = getUtility(IRegistry)
        settings = registry.forInterface(IStatusMessageConfigForm, check=False)

        for field_name in getFieldNames(IStatusMessageConfigForm):
            if field_name in data:
                setattr(settings, field_name, data[field_name])

        return createResponse(states.SuccessState())

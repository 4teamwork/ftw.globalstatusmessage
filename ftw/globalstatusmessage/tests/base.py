from Products.PloneTestCase import ptc
from ftw.globalstatusmessage.tests.layer import gsm_integration_layer


class GSMTestCase(ptc.PloneTestCase):
    """Base class for integration tests."""

    layer = gsm_integration_layer

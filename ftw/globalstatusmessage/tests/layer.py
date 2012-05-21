from collective.testcaselayer.ptc import BasePTCLayer, ptc_layer
# from ftw.globalstatusmessage import tests

class GSMIntegrationLayer(BasePTCLayer):
    """Layer for integration tests."""

    def afterSetUp(self):

        # Load testing zcml (optional)
        # self.loadZCML('testing.zcml', package=tests)

        # installPackage() is *only* necessary for packages outside
        # the Products.* namespace which are also declared as Zope 2 products,
        # using <five:registerPackage /> in ZCML.
        # installPackage('ftw.globalstatusmessage')

        # # Load GS profile
        # import pdb; pdb.set_trace( )
        self.addProfile('ftw.globalstatusmessage:default')

    def beforeTearDown(self):
        pass

gsm_integration_layer = GSMIntegrationLayer(bases=[ptc_layer])

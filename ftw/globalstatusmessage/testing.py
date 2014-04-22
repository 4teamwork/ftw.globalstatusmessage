from plone.app.testing import FunctionalTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from zope.configuration import xmlconfig


class StatusmessageLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        import ftw.globalstatusmessage
        xmlconfig.file('configure.zcml',
                       ftw.globalstatusmessage,
                       context=configurationContext)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'ftw.globalstatusmessage:default')


STATUSMESSAGE_FIXTURE = StatusmessageLayer()
STATUSMESSAGE_FUNCTIONAL = FunctionalTesting(
    bases=(STATUSMESSAGE_FIXTURE, ),
    name="ftw.globalstatusmessage:functional")

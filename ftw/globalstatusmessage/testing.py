from ftw.builder.testing import BUILDER_LAYER
from ftw.builder.testing import functional_session_factory
from ftw.builder.testing import set_builder_session_factory
from plone.app.testing import FunctionalTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from zope.configuration import xmlconfig
import logging
import sys


handler = logging.StreamHandler(sys.stderr)
logging.root.addHandler(handler)


class ZCMLLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        import ftw.globalstatusmessage
        xmlconfig.file('configure.zcml',
                       ftw.globalstatusmessage,
                       context=configurationContext)

STATUSMESSAGE_ZCML_LAYER = ZCMLLayer()
STATUSMESSAGE_ZCML_FUNCTIONAL = FunctionalTesting(
    bases=(STATUSMESSAGE_ZCML_LAYER, ),
    name="ftw.globalstatusmessage:zcml:functional")


class InstallationLayer(PloneSandboxLayer):

    defaultBases = (STATUSMESSAGE_ZCML_LAYER, BUILDER_LAYER)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'ftw.globalstatusmessage:default')


STATUSMESSAGE_FIXTURE = InstallationLayer()
STATUSMESSAGE_FUNCTIONAL = FunctionalTesting(
    bases=(STATUSMESSAGE_FIXTURE,
           set_builder_session_factory(functional_session_factory)),
    name="ftw.globalstatusmessage:functional")

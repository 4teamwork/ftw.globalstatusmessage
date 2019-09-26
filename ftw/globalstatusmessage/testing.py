from ftw.builder.testing import BUILDER_LAYER
from ftw.builder.testing import functional_session_factory
from ftw.builder.testing import set_builder_session_factory
from plone.app.testing import applyProfile, PLONE_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing.z2 import installProduct
from plone.testing.z2 import ZSERVER_FIXTURE
from Products.CMFPlone.utils import getFSVersionTuple
from zope.configuration import xmlconfig
import logging
import sys

handler = logging.StreamHandler(sys.stderr)
logging.root.addHandler(handler)


class ZCMLLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, ZSERVER_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        xmlconfig.string(
            '<configure xmlns="http://namespaces.zope.org/zope">'
            '  <include package="z3c.autoinclude" file="meta.zcml" />'
            '  <includePlugins package="plone" />'
            '  <includePluginsOverrides package="plone" />'
            '</configure>',
            context=configurationContext)

        installProduct(app, 'ftw.globalstatusmessage')

STATUSMESSAGE_ZCML_LAYER = ZCMLLayer()
STATUSMESSAGE_ZCML_FUNCTIONAL = FunctionalTesting(
    bases=(STATUSMESSAGE_ZCML_LAYER, ),
    name="ftw.globalstatusmessage:zcml:functional")


class InstallationLayer(PloneSandboxLayer):

    defaultBases = (STATUSMESSAGE_ZCML_LAYER, BUILDER_LAYER)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'ftw.globalstatusmessage:default')

        if getFSVersionTuple() > (5, ):
            applyProfile(portal, 'plone.app.contenttypes:default')

STATUSMESSAGE_FIXTURE = InstallationLayer()
STATUSMESSAGE_FUNCTIONAL = FunctionalTesting(
    bases=(STATUSMESSAGE_FIXTURE,
           set_builder_session_factory(functional_session_factory)),
    name="ftw.globalstatusmessage:functional")

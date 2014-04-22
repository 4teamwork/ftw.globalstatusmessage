from ftw.globalstatusmessage.interfaces import IStatusMessageConfigForm
from ftw.upgrade import UpgradeStep
from zope.component import getSiteManager
from zope.component import queryUtility
import logging


LOG = logging.getLogger('ftw.globalstatusmessage.upgrades:1003')


class RemoveUtility(UpgradeStep):

    def __call__(self):
        utility = queryUtility(IStatusMessageConfigForm,
                               name='Global_Statusmessage')

        if utility:
            LOG.info('Removing IStatusMessageConfigForm utility.')
            sitemanager = getSiteManager()
            sitemanager.unregisterUtility(
                component=utility,
                provided=IStatusMessageConfigForm,
                name='Global_Statusmessage')

        else:
            LOG.info('IStatusMessageConfigForm utility already removed.')

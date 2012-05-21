from ftw.globalstatusmessage.interfaces import IStatusMessageConfigForm
from ftw.globalstatusmessage.config import FormAdapter


def setup_site(portal):
    control
    sm = portal.getSite()
    sitemanager = sm.getSiteManager()
    test = sitemanager.queryUtility(IStatusMessageConfigForm,
        name='Global_Statusmessage')
    if not test:
        sitemanager.registerUtility(FormAdapter,
            IStatusMessageConfigForm, 'Global_Statusmessage')


def control(context):
    if context.readDataFile('ftw.globalstatusmessage_various.txt') is None:
        return

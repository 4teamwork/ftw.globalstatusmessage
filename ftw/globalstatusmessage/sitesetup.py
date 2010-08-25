from ftw.globalstatusmessage.interfaces import IStatusMessageConfigForm
from ftw.globalstatusmessage.config import FormAdapter


def setup_site(portal):
    # import pdb; pdb.set_trace( )
    control
    sm = portal.getSite()
    sitemanager = sm.getSiteManager()
    test= sitemanager.queryUtility(IStatusMessageConfigForm,
     name='Global_Statusmessage')
    # import pdb; pdb.set_trace()
    if not test:
        sitemanager.registerUtility(FormAdapter,
        IStatusMessageConfigForm, 'Global_Statusmessage')


def control(context):
    if context.readDataFile('ftw.globalstatusmessage_various.txt') is None:
        return

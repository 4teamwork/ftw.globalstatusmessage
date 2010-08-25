from ftw.globalstatusmessage.interfaces import IStatusMessageConfigForm
from ftw.globalstatusmessage.config import FormAdapter


def setup_site(portal):
    import pdb; pdb.set_trace( )
    control
    sm = portal.getSite()
    sitemanager = sm.getSiteManager()
    # import pdb; pdb.set_trace()
    if not sitemanager.queryUtility(IStatusMessageConfigForm,
     name='Global_Statusmessage'):
        sitemanager.registerUtility(FormAdapter(),
        IStatusMessageConfigForm, 'Global_Statusmessage')


def control(context):
    if context.readDataFile('ftw.globalstatusmessage_various.txt') is None:
        return

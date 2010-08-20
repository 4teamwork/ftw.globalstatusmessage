from ftw.globalstatusmessage.interfaces import IStatusMessageConfigForm
from ftw.globalstatusmessage.config import FormAdapter

def setup_site(portal):
    
    sm = portal.getSite()
    sitemanager = sm.getSiteManager()
    # import pdb; pdb.set_trace()     
    if not sitemanager.queryUtility(IStatusMessageConfigForm, name='Global_Statusmessage'):
        sitemanager.registerUtility(FormAdapter(),
                        IStatusMessageConfigForm,
                       'Global_Statusmessage')
                       
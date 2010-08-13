from ftw.globalstatusmessage.interfaces import ISillyConfiguration
from ftw.globalstatusmessage.config import SillyConfiguration

def setup_site(portal):
  sm = portal.getSiteManager()

  if not sm.queryUtility(interfaces.iglobalstatusmessage, name='Global_Statusmessage'):
    sm.registerUtility(SillyConfiguration(),
                       interfaces.ISillyConfiguration,
                       'Global_Statusmessage')

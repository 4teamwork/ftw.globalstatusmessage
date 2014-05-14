from Products.CMFCore.utils import getToolByName


def import_various(context):
    portal = context.getSite()
    action = context.readDataFile('ftw.globalstatusmessage.various.txt')
    action = action.strip() if action else None

    if action == 'uninstall':
        uninstall_controlpanel(portal)
        uninstall_property_sheet(portal)


def uninstall_controlpanel(portal):
    controlpanel = getToolByName(portal, 'portal_controlpanel')
    controlpanel.unregisterConfiglet('globalstatusmessage')


def uninstall_property_sheet(portal):
    properties = getToolByName(portal, 'portal_properties')
    if 'ftw_globalstatusmessage_properties' in properties.objectIds():
        properties.manage_delObjects(['ftw_globalstatusmessage_properties'])

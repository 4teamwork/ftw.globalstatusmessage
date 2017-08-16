import re
from plone import api


def is_path_included(path, included_paths, excluded_paths):
    """Helper function for testing whether a path is in within any
    container in included_paths or in excluded_paths.

    The nearest container path wins.
    If the path is not in any of included_paths or excluded_paths,
    ``True`` is returned as default.
    """
    sites = {'/': True}
    sites.update(dict((path, True) for path in included_paths))
    sites.update(dict((path, False) for path in excluded_paths))

    matching_sites = [site_path for site_path in sites.keys()
                      if path.startswith(site_path)]
    matching_sites.sort()
    return sites[matching_sites[-1]]


def is_profile_installed(profileid):
    """
    Checks whether a generic setup profile is installed.
    Respects product uninstallation via quickinstaller.

    Inspired by `ftw.upgrade.step.UpgradeStep#is_profile_installed`.
    """
    profileid = re.sub(r'^profile-', '', profileid)
    portal_setup = api.portal.get_tool('portal_setup')

    try:
        profileinfo = portal_setup.getProfileInfo(profileid)
    except KeyError:
        return False

    if not is_product_installed(profileinfo['product']):
        return False

    version = portal_setup.getLastVersionForProfile(profileid)
    return version != 'unknown'


def is_product_installed(product_name):
    """
    Check whether a product is installed.

    Inspired by `ftw.upgrade.step.UpgradeStep#is_product_installed`.
    """
    quickinstaller = api.portal.get_tool('portal_quickinstaller')
    return quickinstaller.isProductInstallable(product_name) and \
        quickinstaller.isProductInstalled(product_name)

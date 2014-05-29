

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

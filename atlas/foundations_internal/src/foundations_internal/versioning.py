

def _foundations_version():
    import pkg_resources
    try:
        return pkg_resources.get_distribution('dessa_foundations').version
    except pkg_resources.DistributionNotFound:
        return 'no-version-installed'

__version__ = _foundations_version()
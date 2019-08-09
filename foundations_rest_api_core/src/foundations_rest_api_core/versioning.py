from pkg_resources import get_distribution, DistributionNotFound
try:
    __version__ = get_distribution('foundations_rest_api_core').version
except DistributionNotFound:
    __version__ = None
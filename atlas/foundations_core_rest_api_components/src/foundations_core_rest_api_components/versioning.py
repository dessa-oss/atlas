from pkg_resources import get_distribution, DistributionNotFound
try:
    __version__ = get_distribution('foundations_core_rest_api_components').version
except DistributionNotFound:
    __version__ = None
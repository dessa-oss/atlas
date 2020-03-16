from pkg_resources import get_distribution, DistributionNotFound
try:
    __version__ = get_distribution('foundations_gcp').version
except DistributionNotFound:
    __version__ = None
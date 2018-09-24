from pkg_resources import get_distribution, DistributionNotFound
try:
    __version__ = get_distribution('foundations_ssh').version
except DistributionNotFound:
    __version__ = None
"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Jinnah Ali-Clarke <j.ali-clarke@dessa.com>, 10 2018
"""


def _foundations_version():
    import pkg_resources
    try:
        return pkg_resources.get_distribution('dessa_foundations').version
    except pkg_resources.DistributionNotFound:
        return 'no-version-installed'

__version__ = _foundations_version()
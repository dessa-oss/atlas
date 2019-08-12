"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from pkg_resources import get_distribution, DistributionNotFound
try:
    __version__ = get_distribution('foundations_orbit_rest_api').version
except DistributionNotFound:
    __version__ = None
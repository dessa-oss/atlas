"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_contrib.authentication.authentication_client import (
    AuthenticationClient,
)
from foundations_contrib.authentication.utils import get_token_from_header


def is_string(string):
    return isinstance(string, str)

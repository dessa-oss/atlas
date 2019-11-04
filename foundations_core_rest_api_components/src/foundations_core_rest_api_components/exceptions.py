"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 06 2019
"""

class AuthError(Exception):
    """An exception class to handle authentication/authorization errors."""
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class Session(object):

    @staticmethod
    def auth(password):
        """
        Checks if password matches environment variable.

        Input: Password to check

        Returns: Status code
        """
        import os
        if password == os.environ.get('FOUNDATIONS_GUI_PASSWORD', None):
            return 200
        else:
            return 401
        

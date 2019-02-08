"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class Session(object):

    def __init__(self):
        pass

    @staticmethod
    def auth(password):
        import os
        if password == os.environ.get('GUIPASSWORD', None):
            return 200
        else:
            return 401
        

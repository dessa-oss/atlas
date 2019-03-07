"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 11 2018
"""

class MessageRouteListener(object):
    """
    Template Listener to subscribe to a MessageRoute
    """
    
    def call(self, message):
        """
        Method returns message it was called with

        Arguments:
            message {json seriablizable data} -- message for the listener to return
        """
        return message
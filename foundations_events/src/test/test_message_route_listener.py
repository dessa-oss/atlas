"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 11 2018
"""

from foundations_spec import *
from foundations_events.message_route_listener import MessageRouteListener

class TestMessageRouteListener(Spec):

    def test_call_method(self):
        test_listener = MessageRouteListener()
        self.assertEqual(test_listener.call('message'), 'message')

    def test_call_method_diff_val(self):
        test_listener = MessageRouteListener()
        self.assertEqual(test_listener.call('diff message'), 'diff message')
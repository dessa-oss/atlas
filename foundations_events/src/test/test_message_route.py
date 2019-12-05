"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 11 2018
"""

from foundations_spec import *

from foundations_events.message_route import MessageRoute
from foundations_events.message_route_listener import MessageRouteListener


class TestMessageRoute(Spec):

    route_listener_call_mock = let_patch_mock('foundations_events.message_route_listener.MessageRouteListener.call')

    @let
    def message_listener(self):
        return MessageRouteListener()

    @let
    def message_listener_two(self):
        return MessageRouteListener()

    @set_up
    def set_up(self):
        self.test_route = MessageRoute('event1')

    def test_get_name(self):
        self.assertEqual('event1', self.test_route.get_name())

    def test_add_and_push_message_to_listener(self):
        self.test_route.add_listener(self.message_listener)
        self.test_route.push_message('message', 123, None)
        self.route_listener_call_mock.assert_called_once_with('message', 123, None)
    
    def test_add_and_push_different_message_to_listener(self):
        self.test_route.add_listener(self.message_listener)
        self.test_route.push_message('another message', 1234, 'metametameta')
        self.route_listener_call_mock.assert_called_once_with('another message', 1234, 'metametameta')
    
    def test_add_and_push_message_multi_listener(self):
        self.test_route.add_listener(self.message_listener)
        self.test_route.add_listener(self.message_listener_two)
        self.test_route.push_message('message', 1234, None)
        self.route_listener_call_mock.assert_has_calls([call('message', 1234, None), call('message', 1234, None)])
        


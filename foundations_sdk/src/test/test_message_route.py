"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 11 2018
"""

import unittest
from mock import patch, call

import foundations
from foundations.message_route import MessageRoute
from foundations.message_route_listener import MessageRouteListener

class TestMessageRoute(unittest.TestCase):
    
    def setUp(self):
        self.test_route = MessageRoute('event1')

    def test_get_name(self):
        self.assertEqual('event1', self.test_route.get_name())
    
    @patch.object(MessageRouteListener, 'call')
    def test_add_and_push_message_to_listener(self, mock):
        mock_listener = MessageRouteListener()
        self.test_route.add_listener(mock_listener)
        self.test_route.push_message('message')
        mock.assert_called_once_with('message')
    
    @patch.object(MessageRouteListener, 'call')
    def test_add_and_push_different_message_to_listener(self, mock):
        self.test_route.add_listener(MessageRouteListener())
        self.test_route.push_message('another message')
        mock.assert_called_once_with('another message')
    
    @patch.object(MessageRouteListener, 'call')
    def test_add_and_push_message_multi_listener(self, mock):
        self.test_route.add_listener(MessageRouteListener())
        self.test_route.add_listener(MessageRouteListener())
        self.test_route.push_message('message')
        mock.assert_has_calls([call('message'), call('message')])
        


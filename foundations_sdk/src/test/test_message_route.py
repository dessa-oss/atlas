"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 11 2018
"""

import unittest
from mock import patch, call

import foundations
import time
from foundations.message_route import MessageRoute
from foundations.message_route_listener import MessageRouteListener

class TestMessageRoute(unittest.TestCase):
    
    def setUp(self):
        self.test_route = MessageRoute('event1')

    def test_get_name(self):
        self.assertEqual('event1', self.test_route.get_name())
    
    @patch('time.time')
    @patch.object(MessageRouteListener, 'call')
    def test_add_and_push_message_to_listener(self, mock, mock_time):
        mock_time.return_value = 123
        mock_listener = MessageRouteListener()
        self.test_route.add_listener(mock_listener)
        self.test_route.push_message('message', None)
        mock.assert_called_once_with('message', 123, None)
    
    @patch('time.time')
    @patch.object(MessageRouteListener, 'call')
    def test_add_and_push_different_message_to_listener(self, mock, mock_time):
        mock_time.return_value = 1234
        self.test_route.add_listener(MessageRouteListener())
        self.test_route.push_message('another message', 'metametameta')
        mock.assert_called_once_with('another message', 1234, 'metametameta')
    
    @patch('time.time')
    @patch.object(MessageRouteListener, 'call')
    def test_add_and_push_message_multi_listener(self, mock, mock_time):
        mock_time.return_value = 1234
        self.test_route.add_listener(MessageRouteListener())
        self.test_route.add_listener(MessageRouteListener())
        self.test_route.push_message('message', None)
        mock.assert_has_calls([call('message', 1234, None), call('message', 1234, None)])
        


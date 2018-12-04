"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 11 2018
"""

import unittest
from mock import patch, call

import foundations
from foundations.message_router import MessageRouter

class TestMessageRouter(unittest.TestCase):

    def setUp(self):
        self.message_router = MessageRouter()

    def tearDown(self):
        self.message_router.reset_routes()

    def test_creates_single_instance(self):
        message_router_2 = MessageRouter()
        self.assertEqual(self.message_router.instance, message_router_2.instance)
    
    class MockListener(object):
        def call(self, message):
            return message

    def test_add_new_listener(self):
        self.message_router.add_listener(self.MockListener(), 'event1')
        self.assertTrue(self.message_router._in_route('event1'))
    
    def test_reset_routes(self):
        self.message_router.add_listener(self.MockListener(), 'event1')
        self.message_router.reset_routes()
        self.assertFalse(self.message_router._in_route('event1'))
        
    def test_add_multiple_listeners(self):
        self.message_router.add_listener(self.MockListener(), 'event1')
        self.message_router.add_listener(self.MockListener(), 'event2')
        self.message_router.add_listener(self.MockListener(), 'event3')
        self.assertTrue(self.message_router._in_route('event1'))
        self.assertTrue(self.message_router._in_route('event2'))
        self.assertTrue(self.message_router._in_route('event3'))
    
    @patch.object(foundations.message_route.MessageRoute, 'push_message')
    def test_message_not_pushed_if_no_listeners(self, mock):
        self.message_router.push_message('event1', 'message')
        mock.assert_not_called()
    
    @patch.object(foundations.message_route.MessageRoute, 'push_message')
    def test_message_sent_to_listener(self, mock):
        self.message_router.add_listener(self.MockListener(), 'event1')
        self.message_router.push_message('event1', 'message')
        mock.assert_called_with('message', None)  
    
    @patch.object(foundations.message_route.MessageRoute, 'push_message')
    def test_message_sent_to_listener_with_metadata(self, mock):
        self.message_router.add_listener(self.MockListener(), 'event1')
        self.message_router.push_message('event1', 'message', {'meta': 'data'})
        mock.assert_called_with('message', {'meta': 'data'}) 
        
    @patch.object(foundations.message_route.MessageRoute, 'push_message')
    def test_messages_sent_to_multiple_listeners(self, mock):
        self.message_router.add_listener(self.MockListener(), 'event1')
        self.message_router.add_listener(self.MockListener(), 'event2')
        self.message_router.push_message('event1', 'message1')
        self.message_router.push_message('event2', 'message2',)
        mock.assert_has_calls([call('message1', None), call('message2', None)])


    

"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 11 2018
"""

from foundations_spec import *

from foundations_events.message_router import MessageRouter
from foundations_events.message_route import MessageRoute


class TestMessageRouter(Spec):

    mock_message_route = let_patch_mock('foundations_events.message_route.MessageRoute.push_message')

    @let_now
    def time_mock(self):
        mock = self.patch('time.time')
        mock.return_value = self.current_time
        
        return mock

    @let
    def current_time(self):
        import random
        return random.randint(2, 999999999)

    @set_up
    def set_up(self):
        self.message_router = MessageRouter()

    @tear_down
    def tear_down(self):
        self.message_router.reset_routes()

    def test_creates_single_instance(self):
        message_router_2 = MessageRouter()
        self.assertEqual(self.message_router.instance,
                         message_router_2.instance)

    class MockListener(object):
        def call(self, message, time, metadata):
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

    def test_message_not_pushed_if_no_listeners(self):
        self.message_router.push_message('event1', 'message')
        self.mock_message_route.assert_not_called()
    
    def test_message_sent_to_listener(self):
        self.message_router.add_listener(self.MockListener(), 'event1')
        self.message_router.push_message('event1', 'message')
        self.mock_message_route.assert_called_with('message', self.current_time, None)  
    
    def test_message_sent_to_listener_with_metadata(self):
        self.message_router.add_listener(self.MockListener(), 'event1')
        self.message_router.push_message('event1', 'message', {'meta': 'data'})
        self.mock_message_route.assert_called_with('message', self.current_time, {'meta': 'data'}) 
    
    def test_message_sent_to_listener_with_timestamp_provided(self):
        self.message_router.add_listener(self.MockListener(), 'event1')
        self.message_router.push_message('event1', 'message', {'meta': 'data'}, timestamp=999)
        self.mock_message_route.assert_called_with('message', 999, {'meta': 'data'}) 
        
    def test_messages_sent_to_multiple_listeners(self):
        self.message_router.add_listener(self.MockListener(), 'event1')
        self.message_router.add_listener(self.MockListener(), 'event2')
        self.message_router.push_message('event1', 'message1')
        self.message_router.push_message('event2', 'message2',)
        self.mock_message_route.assert_has_calls([call('message1', self.current_time, None), call('message2', self.current_time, None)])


    

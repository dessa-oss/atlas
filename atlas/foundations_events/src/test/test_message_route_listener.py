
from foundations_spec import *
from foundations_events.message_route_listener import MessageRouteListener

class TestMessageRouteListener(Spec):

    def test_call_method(self):
        test_listener = MessageRouteListener()
        self.assertEqual(test_listener.call('message'), 'message')

    def test_call_method_diff_val(self):
        test_listener = MessageRouteListener()
        self.assertEqual(test_listener.call('diff message'), 'diff message')

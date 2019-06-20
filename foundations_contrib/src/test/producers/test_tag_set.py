"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations_contrib.producers.tag_set import TagSet

class TestTagSet(Spec):

    class MockMessageRouter(object):
        def __init__(self):
            self.set_tag = None

        def push_message(self, name, message):
            self.set_tag = {name: message}

    @let
    def message_router(self):
        return self.MockMessageRouter()

    @let
    def job_id(self):
        return self.faker.uuid4()

    @let
    def tag_name(self):
        return self.faker.word()

    @let
    def tag_value(self):
        return self.faker.random.random()

    @let
    def message(self):
        return {
            'job_id': self.job_id, 
            'key': self.tag_name, 
            'value': self.tag_value
        }
    
    def test_push_message_pushes_message_to_message_router(self):
        tag_set_producer = TagSet(self.message_router, self.job_id, self.tag_name, self.tag_value)
        tag_set_producer.push_message()
        self.assertEqual({'job_tag': self.message}, self.message_router.set_tag)
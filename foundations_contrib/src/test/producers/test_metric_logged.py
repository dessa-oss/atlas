"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations_contrib.producers.metric_logged import MetricLogged

class TestMetricLogged(Spec):
    
    class MockMessageRouter(object):
        def __init__(self):
            self.logged_metric = None

        def push_message(self, name, message):
            self.logged_metric = {name: message}

    @let
    def message_router(self):
        return self.MockMessageRouter()

    @let
    def project_name(self):
        return self.faker.word()

    @let
    def job_id(self):
        return self.faker.uuid4()

    @let
    def metric_key(self):
        return self.faker.word()

    @let
    def metric_value(self):
        return self.faker.random.random()

    @let
    def message(self):
        return {
            'project_name': self.project_name, 
            'job_id': self.job_id, 
            'key': self.metric_key, 
            'value': self.metric_value
        }

    def test_push_message_pushes_message_to_message_router(self):
        message_logged_producer = MetricLogged(self.message_router, self.project_name, self.job_id, self.metric_key, self.metric_value)
        message_logged_producer.push_message()
        self.assertEqual({'job_metrics': self.message}, self.message_router.logged_metric)

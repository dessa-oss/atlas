"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 11 2018
"""
import coverage

cov = coverage.Coverage()
cov.start()

from test.test_message_route import TestMessageRoute
from test.test_message_route_listener import TestMessageRouteListener
from test.test_message_router import TestMessageRouter

cov.stop()
cov.save()

cov.html_report(directory='../../coverage_results/foundations_events')
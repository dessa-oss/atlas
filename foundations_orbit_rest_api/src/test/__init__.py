"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""
import coverage

cov = coverage.Coverage()
cov.start()


import os

os.environ['TZ'] = 'EST'

from test.test_global_state import TestGlobalState
from test.test_production_metrics import TestProductionMetrics
from test.v1 import *

cov.stop()
cov.save()

cov.html_report(directory='../../coverage_results/foundations_orbit_rest_api')
"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 11 2018
"""
import coverage

cov = coverage.Coverage()
cov.start()

from test.config import *
from test.test_job_deployment import TestJobDeployment

cov.stop()
cov.save()

cov.html_report(directory='../../coverage_results/foundations_scheduler_plugin')
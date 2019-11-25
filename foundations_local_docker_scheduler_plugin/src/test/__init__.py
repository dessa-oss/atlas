"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""
import coverage

cov = coverage.Coverage()
cov.start()

from test.test_bundle_deployment import TestBundleDeployment
from test.test_cron_job_scheduler import TestCronJobScheduler

cov.stop()
cov.save()

cov.html_report(directory='../../coverage_results/foundations_local_docker_scheduler')
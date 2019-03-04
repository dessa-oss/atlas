"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


import foundations

import acceptance.config
from acceptance.test_pipeline_interface import TestPipelineInterface
from acceptance.test_run_job import TestRunJob
from acceptance.test_duplicate_job_source import TestDuplicateJobSource
from acceptance.test_run_job_with_unserializable_outputs import TestRunJobWithUnserializableOutputs
from acceptance.test_recursion_limit import TestRecursionLimit
from acceptance.test_job_data_producers import TestJobDataProducers
from acceptance.test_cli_init import TestCLIInit
from acceptance.test_job_uses_venv_created_by_foundations import TestJobUsesVenvCreatedByFoundations
from acceptance.prototype import *
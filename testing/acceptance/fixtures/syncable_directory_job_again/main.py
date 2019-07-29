"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import foundations

parameters = foundations.load_parameters(log_parameters=False)
job_id = parameters['source_job_id']

first_directory = foundations.create_syncable_directory('some data', 'results', source_job_id=job_id)
first_directory.upload()

second_directory = foundations.create_syncable_directory('some metadata', 'metadata', source_job_id=job_id)
second_directory.upload()
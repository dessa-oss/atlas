"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def cancel(job_id):
    import subprocess
    import foundations_contrib

    subprocess.run(['bash', './delete_job.sh', job_id], cwd=foundations_contrib.root() / 'resources/jobs')
    
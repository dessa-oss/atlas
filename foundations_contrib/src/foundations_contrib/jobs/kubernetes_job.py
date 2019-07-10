"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def cancel(job_id):
    import subprocess
    import foundations_contrib
    from foundations_contrib.global_state import redis_connection

    subprocess.run(['bash', './delete_job.sh', job_id], cwd=foundations_contrib.root() / 'resources/jobs', capture_output=True)
    project_name = redis_connection.get(f'jobs:{job_id}:project').decode()
    redis_connection.srem(f'project:{project_name}:jobs:running', job_id)
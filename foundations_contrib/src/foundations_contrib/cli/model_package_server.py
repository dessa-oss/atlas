"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


def deploy(project_name, job_id):
    from subprocess import run
    import foundations_contrib
    
    run(['bash', './deploy_serving.sh', project_name, job_id], cwd=foundations_contrib.root() / 'resources/model_serving')

def destroy(project_name, model_name):
    from subprocess import run
    import foundations_contrib
    
    run(['bash', './remove_deployment.sh', project_name, model_name], cwd=foundations_contrib.root() / 'resources/model_serving')

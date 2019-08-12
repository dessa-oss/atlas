"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


def deploy(project_name, model_name, project_directory):
    from subprocess import run
    import foundations_contrib
    
    run(['bash', './orbit/deploy_serving.sh', project_name, model_name, project_directory], cwd=foundations_contrib.root() / 'resources/model_serving/orbit')
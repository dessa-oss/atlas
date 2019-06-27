"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Foundations Team <pairing@dessa.com>, 06 2018
"""

def deploy(project_name=None):
    import os
    import os.path as path

    import foundations

    if project_name is None:
        cwd_path = os.getcwd()
        project_name = path.basename(cwd_path)

    foundations.set_project_name(project_name)
    foundations.config_manager.add_simple_config_path('~/.foundations/config/local.config.yaml')
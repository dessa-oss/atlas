"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Foundations Team <pairing@dessa.com>, 06 2018
"""

def deploy():
    import os
    import os.path as path

    import foundations

    cwd_path = os.getcwd()
    cwd_name = path.basename(cwd_path)

    foundations.set_project_name(cwd_name)
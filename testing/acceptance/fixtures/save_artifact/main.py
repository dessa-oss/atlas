"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import os
import os.path as path

import foundations

cwd = os.getcwd()

foundations.save_artifact(filepath=path.join(cwd, 'cool-artifact.txt'))
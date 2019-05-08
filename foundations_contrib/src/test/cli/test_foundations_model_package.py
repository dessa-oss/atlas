"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest
from mock import Mock

from foundations_spec.helpers import let, let_now, let_patch_mock
from foundations_spec.helpers.spec import Spec


class TestFoundationsModelPackage(Spec):
    def test_foundations_model_package_run_method_calls_
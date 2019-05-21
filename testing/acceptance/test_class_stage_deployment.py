"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

class TestClassStageDeployment(Spec):
    
    class TestClass(object):
        def __init__(self):
            pass

    def test_can_create_stage_with_class(self):
        import foundations

        test_stage = foundations.create_stage(self.TestClass)()
        test_stage.run()

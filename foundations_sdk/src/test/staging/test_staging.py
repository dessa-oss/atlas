"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

class TestStaging(Spec):

    @set_up
    def set_up(self):
        self._called = False
        self._args = None
        self._kwargs = None

    def test_create_stage_creates_stage(self):
        from foundations.staging import create_stage
        from foundations.stage_connector_wrapper import StageConnectorWrapper
        
        stage = create_stage(self._method)()
        self.assertTrue(isinstance(stage, StageConnectorWrapper))

    def test_create_stage_creates_stage_with_method(self):
        from foundations.staging import create_stage

        stage = create_stage(self._method)().run_same_process()
        self.assertTrue(self._called)

    def test_create_stage_creates_stage_with_args(self):
        from foundations.staging import create_stage

        create_stage(self._method)('hello').run_same_process()
        self.assertEqual(('hello',), self._args)

    def test_create_stage_creates_stage_with_args_different_args(self):
        from foundations.staging import create_stage

        create_stage(self._method)('goodbye', 'friend').run_same_process()
        self.assertEqual(('goodbye', 'friend'), self._args)

    def test_create_stage_creates_stage_with_kwargs(self):
        from foundations.staging import create_stage

        create_stage(self._method)(nope='yup', maybe='possibly').run_same_process()
        self.assertEqual({'nope': 'yup', 'maybe': 'possibly'}, self._kwargs)

    def test_global_create_stage_uses_create_stage(self):
        from foundations.staging import create_stage
        import foundations

        self.assertEqual(foundations.create_stage, create_stage)

    def _method(self, *args, **kwargs):
        self._called = True
        self._args = args
        self._kwargs = kwargs
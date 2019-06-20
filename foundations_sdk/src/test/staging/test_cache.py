"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
from foundations.staging import cache

class TestCache(Spec):
    
    mock_cached_stage_result = let_patch_mock_with_conditional_return('foundations.staging.cached_stage_result')
    mock_foundations_stage = let_patch_mock_with_conditional_return('foundations.staging.foundations_stage')

    mock_stage = let_mock()
    mock_cached_value = let_mock()

    mock_function = let_mock()

    @let
    def random_args(self):
        return self.faker.words()

    @let
    def random_kwargs(self):
        return self.faker.pydict()

    @set_up
    def set_up(self):
        self.mock_cached_stage_result.return_when(self.mock_cached_value, self.mock_stage)
        self.mock_foundations_stage.return_when(self.mock_stage, self.mock_function, *self.random_args, **self.random_kwargs)


    def test_creates_function_that_returns_cached_value(self):
        cached_function = cache(self.mock_function)
        self.assertEqual(self.mock_cached_value, cached_function(*self.random_args, **self.random_kwargs))


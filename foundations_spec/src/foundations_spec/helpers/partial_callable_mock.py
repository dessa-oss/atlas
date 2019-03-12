"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from mock import Mock

class PartialCallableMock(Mock):

    def assert_called_with_partial(self, *args, **kwargs):
        self._raise_if_not_called(args, kwargs)
        self._raise_if_call_does_not_match(args, kwargs)
    
    def _raise_if_call_does_not_match(self, args, kwargs):
        expected = self._call_matcher((args, kwargs))
        expected_args, expected_kwargs = expected
        actual_args, actual_kwargs = self._call_matcher(self.call_args)
        both_args_match = self._args_match(expected_args, actual_args) and self._kwargs_match(expected_kwargs, actual_kwargs)
        if not both_args_match:
            cause = expected if isinstance(expected, Exception) else None
            raise AssertionError(self._partial_error_message(args, kwargs)) from cause
    
    def _raise_if_not_called(self, args, kwargs):
        if self.call_args is None:
            expected = self._format_mock_call_signature(args, kwargs)
            raise AssertionError('Expected call: {}\nNot called'.format(expected))

    def _partial_error_message(self, args, kwargs):
        return self._format_mock_failure_message(args, kwargs)

    @staticmethod
    def _args_match(expected_args, actual_args):
        actual_arg_index = 0
        for arg in expected_args:
            found, actual_arg_index = PartialCallableMock._find_arg(arg, actual_args, actual_arg_index)
            if not found:
                return False
        return True

    @staticmethod
    def _find_arg(arg, actual_args, actual_arg_index):
        while actual_arg_index < len(actual_args):
            actual_arg_index += 1 
            if actual_args[actual_arg_index-1] == arg:
                return True, actual_arg_index
        return False, actual_arg_index

    @staticmethod
    def _kwargs_match(expected_kwargs, actual_kwargs):
        return expected_kwargs.items() <= actual_kwargs.items()
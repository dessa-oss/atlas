"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class ArgumentFiller(object):

    def __init__(self, argument_fill, *args, **kwargs):
        self._argument_fill = argument_fill
        self.args = args
        self.kwargs = kwargs

    def fill(self, **kwargs):
        new_args = []
        for arg in self.args:
            self._fill_arg(new_args, arg, kwargs)

        new_kwargs = {}
        for keyword, arg in self.kwargs.items():
            self._fill_kwarg(new_kwargs, keyword, arg, kwargs)

        return new_args, new_kwargs

    def _fill_arg(self, new_args, arg, kwargs):
        if not self._argument_fill.fill_arg_template(new_args, arg, kwargs):
            new_args.append(arg)

    def _fill_kwarg(self, new_kwargs, keyword, arg, kwargs):
        if not self._argument_fill.fill_kwarg_template(new_kwargs, keyword, arg, kwargs):
            new_kwargs[keyword] = arg

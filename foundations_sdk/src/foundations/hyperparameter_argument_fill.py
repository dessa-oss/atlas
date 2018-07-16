"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations.hyperparameter import Hyperparameter


class HyperparameterArgumentFill(object):

    def fill_arg_template(self, new_args, arg, kwargs):
        if isinstance(arg, Hyperparameter):
            if arg.name in kwargs:
                new_args.append(kwargs[arg.name])
            return True
        return False

    def fill_kwarg_template(self, new_kwargs, keyword, arg, kwargs):
        if isinstance(arg, Hyperparameter):
            if keyword in kwargs:
                new_kwargs[keyword] = kwargs[keyword]
            return True
        return False

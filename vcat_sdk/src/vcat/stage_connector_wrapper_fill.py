"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from vcat.stage_connector_wrapper import StageConnectorWrapper

class StageConnectorWrapperFill(object):

    def fill_arg_template(self, new_args, arg, kwargs):
        if isinstance(arg, StageConnectorWrapper):
            new_args.append(arg.run_same_process(**kwargs))
            return True
        return False

    def fill_kwarg_template(self, new_kwargs, keyword, arg, kwargs):
        if isinstance(arg, StageConnectorWrapper):
            new_kwargs[keyword] = arg.run_same_process(**kwargs)
            return True
        return False

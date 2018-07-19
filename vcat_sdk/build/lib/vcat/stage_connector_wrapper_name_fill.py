"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from vcat.stage_connector_wrapper import StageConnectorWrapper


class StageConnectorWrapperNameFill(object):

    def fill_arg_template(self, new_args, arg, kwargs):
        if isinstance(arg, StageConnectorWrapper):
            new_args.append({"stage_id": arg._connector.name()})
            return True
        return False

    def fill_kwarg_template(self, new_kwargs, keyword, arg, kwargs):
        if isinstance(arg, StageConnectorWrapper):
            new_kwargs[keyword] = {"stage_id": arg._connector.name()}
            return True
        return False

"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec.helpers.callback import Callback


class let(Callback):

    def assign_value(self, attribute_name, spec_instance):
        value = self.evaluate(spec_instance)
        setattr(spec_instance, attribute_name, value)
        return value
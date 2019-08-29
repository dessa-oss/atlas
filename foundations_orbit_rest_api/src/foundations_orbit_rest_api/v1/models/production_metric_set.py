"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_core_rest_api_components.common.models.property_model import PropertyModel

class ProductionMetricSet(PropertyModel):

    title = PropertyModel.define_property()
    yAxis = PropertyModel.define_property()
    xAxis = PropertyModel.define_property()
    series = PropertyModel.define_property()

    @staticmethod
    def all(project_name):
        from foundations_core_rest_api_components.lazy_result import LazyResult

        def _all():
            return []

        return LazyResult(_all)
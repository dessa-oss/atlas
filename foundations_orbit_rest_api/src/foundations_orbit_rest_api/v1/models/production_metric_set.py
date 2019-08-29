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
            from foundations_orbit_rest_api.production_metrics import all_production_metrics

            model_name = ProductionMetricSet.models_from_project(project_name)
            if model_name is None:
                return []

            model_metrics = all_production_metrics(project_name, model_name)
            metric_name, metric_pairs = list(model_metrics.items())[0]

            metric_columns = []
            metric_values = []
            
            if metric_pairs:
                metric_column, metric_value = metric_pairs[0]
                metric_columns.append(metric_column)
                metric_values.append(metric_value)

            metric_set = ProductionMetricSet(
                title={'text': f'{metric_name} over time'},
                yAxis={'title': {'text': metric_name}},
                xAxis={'categories': metric_columns},
                series=[{'data': metric_values, 'name': model_name}]
            )
            
            return [metric_set]

        return LazyResult(_all)
    
    @staticmethod
    def models_from_project(project_name):
        from foundations_contrib.global_state import redis_connection
        model_names = redis_connection.keys(f'projects:{project_name}:models:*:production_metrics')

        if not model_names:
            return None
        return model_names[0].decode().split(':')[3]
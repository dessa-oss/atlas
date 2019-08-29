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
        return LazyResult(lambda: ProductionMetricSet._all_internal(project_name))
    
    @staticmethod
    def _all_internal(project_name):
        from foundations_orbit_rest_api.production_metrics import all_production_metrics

        model_names = ProductionMetricSet._models_from_project(project_name)
        
        intermediate_data_hierarchy = {}

        for model_name in model_names:                
            model_metrics = all_production_metrics(project_name, model_name)
            
            for metric_name, metric_pairs in model_metrics.items():
                ProductionMetricSet._append_to_metric_set_series(intermediate_data_hierarchy, metric_name, model_name, metric_pairs)

        return list(intermediate_data_hierarchy.values())

    @staticmethod
    def _append_to_metric_set_series(intermediate_data_hierarchy, metric_name, model_name, metric_pairs):
        metric_columns, metric_values = ProductionMetricSet._unzip_list_of_pairs(metric_pairs)

        if metric_name not in intermediate_data_hierarchy:
            intermediate_data_hierarchy[metric_name] = ProductionMetricSet._metric_set_from_simple_metric_information(metric_name, metric_columns, [])

        intermediate_data_hierarchy[metric_name].series.append({'data': metric_values, 'name': model_name})

    @staticmethod
    def _models_from_project(project_name):
        from foundations_contrib.global_state import redis_connection
        
        model_names = redis_connection.keys(f'projects:{project_name}:models:*:production_metrics')
        return list(map(ProductionMetricSet._model_name_from_redis_key, model_names))

    @staticmethod
    def _model_name_from_redis_key(key):
        return key.decode().split(':')[3]

    @staticmethod
    def _metric_set_from_simple_metric_information(metric_name, metric_columns, metric_series):
        return ProductionMetricSet(
            title={'text': f'{metric_name} over time'},
            yAxis={'title': {'text': metric_name}},
            xAxis={'categories': metric_columns},
            series=metric_series
        )

    @staticmethod
    def _unzip_list_of_pairs(list_of_pairs):
        first_elements = []
        second_elements = []

        for first_element, second_element in list_of_pairs:
            first_elements.append(first_element)
            second_elements.append(second_element)

        return first_elements, second_elements
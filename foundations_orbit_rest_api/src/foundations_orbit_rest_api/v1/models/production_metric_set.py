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
        
        intermediate_data_hierarchy = _IntermediateDataHierarchy()

        for model_name in model_names:                
            model_metrics = all_production_metrics(project_name, model_name)
            intermediate_data_hierarchy.process_model_metrics_with_model_name(model_name, model_metrics)

        return intermediate_data_hierarchy.metric_sets()

    @staticmethod
    def _models_from_project(project_name):
        from foundations_contrib.global_state import redis_connection
        
        model_names = redis_connection.keys(f'projects:{project_name}:models:*:production_metrics')
        return list(map(ProductionMetricSet._model_name_from_redis_key, model_names))

    @staticmethod
    def _model_name_from_redis_key(key):
        return key.decode().split(':')[3]

class _IntermediateDataHierarchy(object):

    def __init__(self):
        self._hierarchy = {}

    def process_model_metrics_with_model_name(self, model_name, model_metrics):
        for metric_name, metric_pairs in model_metrics.items():
            self._append_to_metric_set_series(metric_name, model_name, metric_pairs)

    def metric_sets(self):
        return list(self._hierarchy.values())

    def _append_to_metric_set_series(self, metric_name, model_name, metric_pairs):
        metric_columns, metric_values = _unzip_list_of_pairs(metric_pairs)

        if metric_name not in self._hierarchy:
            self._hierarchy[metric_name] = _metric_set_from_simple_metric_information(metric_name, metric_columns, [])

        self._hierarchy[metric_name].series.append({'data': metric_values, 'name': model_name})

def _unzip_list_of_pairs(list_of_pairs):
    first_elements = []
    second_elements = []

    for first_element, second_element in list_of_pairs:
        first_elements.append(first_element)
        second_elements.append(second_element)

    return first_elements, second_elements

def _metric_set_from_simple_metric_information(metric_name, metric_columns, metric_series):
    return ProductionMetricSet(
        title={'text': f'{metric_name} over time'},
        yAxis={'title': {'text': metric_name}},
        xAxis={'categories': metric_columns},
        series=metric_series
    )
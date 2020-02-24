
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

        monitor_names = ProductionMetricSet._monitors_from_project(project_name)
        
        intermediate_data_hierarchy = _IntermediateDataHierarchy()

        for monitor_name in monitor_names:
            monitor_metrics = all_production_metrics(project_name, monitor_name)
            intermediate_data_hierarchy.process_monitor_metrics_with_monitor_name(monitor_name, monitor_metrics)

        return intermediate_data_hierarchy.metric_sets()

    @staticmethod
    def _monitors_from_project(project_name):
        from foundations_contrib.global_state import redis_connection
        
        monitor_names = redis_connection.keys(f'projects:{project_name}:monitors:*:production_metrics')
        return list(map(ProductionMetricSet._monitor_name_from_redis_key, monitor_names))

    @staticmethod
    def _monitor_name_from_redis_key(key):
        return key.decode().split(':')[3]

class _IntermediateDataHierarchy(object):

    def __init__(self):
        self._hierarchy = {}

    def process_monitor_metrics_with_monitor_name(self, monitor_name, monitor_metrics):
        for metric_name, metric_pairs in monitor_metrics.items():
            self._append_to_metric_set_series(metric_name, monitor_name, metric_pairs)

    def metric_sets(self):
        return list(self._hierarchy.values())

    def _append_to_metric_set_series(self, metric_name, monitor_name, metric_pairs):
        converted_metric_pairs = convert_date_strings_to_timestamps(metric_pairs)
        if metric_name not in self._hierarchy:
            self._hierarchy[metric_name] = _metric_set_from_simple_metric_information(metric_name, [])

        self._hierarchy[metric_name].series.append({'data': converted_metric_pairs, 'name': monitor_name})

def convert_date_strings_to_timestamps(list_of_pairs):
    return [[_convert_date_string_to_timestamp(date_string), second_element] for date_string, second_element in list_of_pairs]

def _metric_set_from_simple_metric_information(metric_name, metric_series):
    return ProductionMetricSet(
        title={'text': f'{metric_name} over time'},
        yAxis={'title': {'text': metric_name}},
        xAxis={'type': 'datetime'},
        series=metric_series
    )

def _convert_date_string_to_timestamp(time):
    from dateutil import parser

    if type(time) == str:
        time = parser.parse(time)

    return time.timestamp() * 1000
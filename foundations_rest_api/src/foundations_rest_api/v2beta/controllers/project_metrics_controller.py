"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_rest_api.utils.api_resource import api_resource

from foundations_core_rest_api_components.lazy_result import LazyResult
from foundations_core_rest_api_components.response import Response

from collections import namedtuple

@api_resource('/api/v2beta/projects/<string:project_name>/overview_metrics')
class ProjectMetricsController(object):

    def index(self):
        return Response('Jobs', LazyResult(self._project_metrics_or_single_metric))

    def _project_metrics_or_single_metric(self):
        if 'metric_name' in self.params:
            return [self._single_metric()]
        else:
            return list(self._get_metrics())

    def _single_metric(self):
        metric_name = self.params['metric_name']
        metrics = self._grouped_metrics()[metric_name]
        return self._metric(metric_name, metrics)

    def _get_metrics(self):
        for metric_name, metrics in self._grouped_metrics().items():
            yield self._metric(metric_name, metrics)
    
    def _metric(self, metric_name, metrics):
        return {
            'metric_name': metric_name,
            'values': metrics
        }

    def _grouped_metrics(self):
        from collections import defaultdict

        grouped_metrics = defaultdict(list)
        for metric in self._sorted_project_metrics():
            grouped_metrics[metric['metric_name']].append([metric['job_id'], metric['value']])
        return grouped_metrics

    def _sorted_project_metrics(self):
        return sorted(self._project_metrics(), key=lambda item: item['timestamp'])

    def _project_metrics(self):
        from foundations_internal.fast_serializer import deserialize

        for metric_key, serialized_metric in self._serialized_project_metrics().items():
            job_id, metric_name = metric_key.decode().split(':')
            timestamp, value = deserialize(serialized_metric)
            yield {
                'job_id': job_id,
                'metric_name': metric_name,
                'timestamp': timestamp,
                'value': value
            }

    def _serialized_project_metrics(self):
        from foundations_contrib.global_state import redis_connection

        project_key = f'projects:{self._project_name()}:metrics'
        return redis_connection.hgetall(project_key)        

    def _project_name(self):
        return self.params['project_name']

from foundations_rest_api.utils.api_resource import api_resource

from foundations_core_rest_api_components.lazy_result import LazyResult
from foundations_core_rest_api_components.response import Response

from collections import namedtuple


@api_resource("/api/v2beta/projects/<string:project_name>/overview_metrics")
class ProjectMetricsController(object):
    def index(self):
        return Response("Jobs", LazyResult(self._project_metrics_or_single_metric))

    def _project_metrics_or_single_metric(self):
        if "metric_name" in self.params:
            return self._multiple_metrics()
        else:
            return self._get_metrics()

    def _multiple_metrics(self):
        grouped_metrics = self._grouped_metrics()
        all_metric_names = list(grouped_metrics.keys())

        metric_names = self.params["metric_name"].split("|")
        metric_query = [
            self._single_metric(metric_name, grouped_metrics)
            for metric_name in metric_names
        ]

        return {"all_metric_names": all_metric_names, "metric_query": metric_query}

    def _single_metric(self, metric_name, grouped_metrics):
        metrics = grouped_metrics[metric_name]
        return self._metric(metric_name, metrics)

    def _get_metrics(self):
        grouped_metrics = self._grouped_metrics()

        all_metric_names = list(grouped_metrics.keys())
        all_metrics = [
            self._metric(metric_name, metrics)
            for metric_name, metrics in grouped_metrics.items()
        ]
        return {"all_metric_names": all_metric_names, "metric_query": all_metrics}

    def _metric(self, metric_name, metrics):
        return {"metric_name": metric_name, "values": metrics}

    def _grouped_metrics(self):
        from collections import defaultdict

        grouped_metrics = defaultdict(list)
        for metric in self._sorted_project_metrics():
            grouped_metrics[metric["metric_name"]].append(
                [metric["job_id"], metric["value"]]
            )
        return grouped_metrics

    def _sorted_project_metrics(self):
        return sorted(self._project_metrics(), key=lambda item: item["timestamp"])

    def _project_metrics(self):
        from foundations_internal.fast_serializer import deserialize

        for metric_key, serialized_metric in self._serialized_project_metrics().items():
            job_id, metric_name = metric_key.decode().split(":")
            timestamp, value = deserialize(serialized_metric)
            yield {
                "job_id": job_id,
                "metric_name": metric_name,
                "timestamp": timestamp,
                "value": value,
            }

    def _serialized_project_metrics(self):
        from foundations_rest_api.global_state import redis_connection

        project_key = f"projects:{self._project_name()}:metrics"
        return redis_connection.hgetall(project_key)

    def _project_name(self):
        return self.params["project_name"]

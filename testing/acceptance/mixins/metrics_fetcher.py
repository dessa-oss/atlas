
class MetricsFetcher(object):

    def _get_metrics_for_all_jobs(self, project_name):
        import foundations
        return foundations.get_metrics_for_all_jobs(project_name)

    def _get_logged_metric(self, project_name, job_id, metric_name):
        all_metrics = self._get_metrics_for_all_jobs(project_name)
        metrics_for_job = all_metrics.loc[all_metrics['job_id'] == job_id].iloc[0]
        return metrics_for_job[metric_name]
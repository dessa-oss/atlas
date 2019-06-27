"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class MetricsFetcher(object):

    def _get_metrics_for_all_jobs(self, project_name):
        import foundations
        return foundations.get_metrics_for_all_jobs(project_name)

    def _get_logged_metric(self, project_name, job_id, metric_name):
        all_metrics = self._get_metrics_for_all_jobs(project_name)
        metrics_for_job = all_metrics.loc[all_metrics['job_id'] == job_id].iloc[0]
        return metrics_for_job[metric_name]
    
    # strike 1 - consider refactoring into own mixin

    def _get_metrics_and_tags_for_all_jobs(self, project_name, ignore_errors=False):
        import pandas
        import foundations.prototype

        try:
            return foundations.prototype.get_metrics_for_all_jobs(project_name)
        except KeyError as ex:
            if ignore_errors and 'job_id' in ex.args:
                return pandas.DataFrame()
            raise

    def _get_tag(self, project_name, job_id, tag_name):
        all_metrics_and_tags = self._get_metrics_and_tags_for_all_jobs(project_name)
        metrics_and_tags_for_job = all_metrics_and_tags.loc[all_metrics_and_tags['job_id'] == job_id].iloc[0]
        return metrics_and_tags_for_job['tag_{}'.format(tag_name)]
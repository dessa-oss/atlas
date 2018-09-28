"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class CompletedJobData(object):
    def __init__(self, context, job_id):
        self._context = context
        self._context.load_stage_log_from_archive()
        self._context.load_provenance_from_archive()
        self._job_id = job_id
        self._project_name = self._context.provenance.project_name

    def load_job(self):
        job_metrics = self._load_job_metrics()
        input_params = self._load_input_params()
        return self._assign_job_param(job_metrics, input_params)
        
    def _load_input_params(self):
        input_params = []
        for stage_uuid, argument in self._stage_arguments():
            parameter = self._job_parameter(stage_uuid, argument)
            input_params.append(parameter)
        return input_params

    def _job_parameter(self, stage_uuid, argument):
        return {'name': argument['name'], 'value': argument['value'], 'stage_uuid': stage_uuid}

    def _stage_arguments(self):
        for stage_uuid, entry in self._stage_hierarchy_entries():
            for argument in entry.stage_args:
                yield stage_uuid, argument

    def _load_job_metrics(self):
        stage_metrics = {}
        for item in self._stage_metrics():
            self._add_metric(stage_metrics, item['key'], item['value'])
        return stage_metrics

    def _stage_metrics(self):
        for stage_context in self._context.stage_contexts.values():
            for item in stage_context.stage_log:
                yield item

    def _assign_job_param(self, stage_metrics, input_params):

        return {
            'project_name': self._project_name,
            'job_id': self._job_id,
            'user': 'Unspecified',
            'job_parameters': self._context.provenance.job_run_data,
            'input_params': input_params,
            'output_metrics': stage_metrics,
            'status': 'Completed',
            'start_time': self._context.global_stage_context.start_time,
            'completed_time': self._context.global_stage_context.end_time
        }

    def _stage_hierarchy_entries(self):
        return self._context.provenance.stage_hierarchy.entries.items()

    def _add_metric(self, metrics, key, value):
        if key in metrics:
            if isinstance(metrics[key], list):
                metrics[key].append(value)
            else:
                metrics[key] = [metrics[key], value]
        else:
            metrics[key] = value
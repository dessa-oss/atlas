"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class InputParameterIndexer(object):
    """
    This class fetches the index rank of each stage_uuid and passes that info to the InputParameterFormatter
    for formatting.
    """

    @staticmethod
    def index_input_parameters(project_name, jobs_data):
        from foundations.global_state import redis_connection
        from foundations_contrib.input_parameter_formatter import InputParameterFormatter

        stage_times = redis_connection.zrange('projects:{}:stage_time'.format(project_name), 0, -1, withscores=True)
        stage_rank = InputParameterIndexer._get_stage_rank(stage_times)

        for job in jobs_data:
            job['input_params'] = InputParameterFormatter(job['input_params'], job['job_parameters'], stage_rank).format_input_parameters()
        return jobs_data

    @staticmethod
    def _get_stage_rank(stage_times):
        stage_uuid_rank = [(key.decode(), index) for index, (key, value) in enumerate(stage_times)]
        stage_uuid_rank = dict(stage_uuid_rank)

        return stage_uuid_rank

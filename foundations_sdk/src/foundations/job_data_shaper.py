"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


class JobDataShaper(object):
    """
    As below
    """

    def __init__(self, jobs_data):
        self._jobs_data = jobs_data

    @staticmethod
    def shape_data(jobs_data):
        """
        This class (hopefully soon deprecated) takes the shape of the Redis data and massages it to look like
        data from the CompletedJobData class

        Arguments:
            jobs_data {list of dictionaries} - List of job data

        Return:
            jobs_data {list of dictionaries} - List of job data, format changed
        """
        for job in jobs_data:
            job['output_metrics'] = JobDataShaper._change_list_to_dict(
                job['output_metrics'])
            job['input_params'] = JobDataShaper._flatten_argument(
                job['input_params'])

        return jobs_data

    @staticmethod
    def _change_list_to_dict(output_metrics):
        output_dict = {}
        for metric in output_metrics:
            output_dict.update({metric[1]: metric[2]})
        return output_dict

    @staticmethod
    def _collapse_to_one_dictionary(params):
        param_dict = {}
        for param in params:
            param_dict.update(param)
        return param_dict

    @staticmethod
    def _flatten_argument(params):
        for param in params:
            param.update(param['argument'])
            del param['argument']
        return params

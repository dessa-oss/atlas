"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


def set_project_name(project_name):
    from foundations.global_state import foundations_context
    foundations_context.set_project_name(project_name)

def get_metrics_for_all_jobs(project_name):
    from foundations.models.completed_job_data_listing import CompletedJobDataListing
    from pandas import DataFrame

    data_frame = DataFrame(CompletedJobDataListing.completed_job_data())

    return data_frame[data_frame['project_name'] == project_name]
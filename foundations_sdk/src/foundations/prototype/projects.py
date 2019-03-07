"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def get_metrics_for_all_jobs(project_name):
    import foundations
    from pandas import DataFrame

    return foundations.get_metrics_for_all_jobs(project_name)
"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

"""
Similar to ResultsReader, get_metrics_for_all_jobs allows you to fetch results
for all jobs under a project that have stored their results in an accessible location (e.g. S3, GS,
local directory). The results are returned in a pandas.DataFrame, making them easy to query and further manipulate. 

In this example, we query results stored on the local filesystem under the "Titanic Survival" project
and return them into a dataframe - this allows for sorting, filtering, and so forth.

Note: Make sure you run a project with a project_name (like the logistic_regression or grid_search example)
before running this module.

See comments below for a walkthrough.
"""

# import utilities to log and fetch the results
from foundations import log_manager, get_metrics_for_all_jobs


def main():
    # get a logger - like using print, but more configurable
    log = log_manager.get_logger(__name__)
    
    # get and print results
    log.info("\n{}".format(get_metrics_for_all_jobs("Titanic Survival")))

if __name__ == '__main__':
    main()
"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def get_metrics_for_all_jobs(project_name):
    """
    Returns metrics and tags for all jobs for a given project. This function is an experimental feature, and is under the foundations.prototype package

    Arguments:
        project_name {string} -- Name of the project to filter by.
        include_input_params {boolean} -- Optional way to specify if metrics should include all model input metrics

    Returns:
        metrics {DataFrame} -- A Pandas DataFrame containing all of the results.

    Raises:
        ValueError -- An exception indicating that the requested project does not exist

    Example:
        ```python
        import foundations
        from algorithms import train_model, print_metrics

        train_model = foundations.create_stage(train_model)
        foundations.set_tag('model', 'CNN')
        model = train_model()

        all_metrics = foundations.prototype.get_metrics_for_all_jobs(job_name)
        print_metrics(all_metrics)
        ```
    """
    import foundations
    from foundations_contrib.global_state import redis_connection
    from foundations.helpers.annotate import annotations_for_multiple_jobs
    from foundations_contrib.redis_pipeline_wrapper import RedisPipelineWrapper
    from pandas import DataFrame

    metrics = foundations.get_metrics_for_all_jobs(project_name)
    metric_rows = list(metrics.T.to_dict().values())

    job_annotations = annotations_for_multiple_jobs(redis_connection, metrics['job_id'])

    for row in metric_rows:
        annotations = job_annotations[row['job_id']]
        for key, value in annotations.items():
            tag_key = 'tag_{}'.format(key)
            row[tag_key] = value
    
    return DataFrame(metric_rows)
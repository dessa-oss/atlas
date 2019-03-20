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
        import foundations.prototype
        from algorithms import train_model, print_metrics

        train_model = foundations.create_stage(train_model)
        foundations.prototype.set_tag('model', 'CNN')
        model = train_model()

        all_metrics = foundations.prototype.get_metrics_for_all_jobs(job_name)
        print_metrics(all_metrics)
        ```
    """
    import foundations
    from foundations_contrib.global_state import redis_connection
    from foundations.prototype.helpers.annotate import annotations_for_multiple_jobs
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

def set_tag(key, value):
    """
    Adds additional static, predetermined information as a tag to the job. This is a way to categorize attributes of a job that is not dynamically generated during runtime.

    Arguments:
        key {str} -- the name of the tag.
        value {number, str, bool, array of [number|str|bool], array of array of [number|str|bool]} -- the value associated with the given tag.

    Returns:
        - This function doesn't return a value.

    Raises:
        - This method doesn't raise any exceptions.

    Notes:
        If a tag is updated multiple times, Foundations will update the tag to the newest value, but return a warning indicating that the
        key has been updated.

    Example:
        ```python
        import foundations
        import foundations.prototype
        from algorithms import train_model_xgboost
        
        train_model = foundations.create_stage(train_model_xgboost)
        model = train_model()
        foundations.prototype.set_tag('model', 'xgboost')
        model.run()
        ```
    """
    from foundations_contrib.global_state import foundations_context, log_manager

    annotations = foundations_context.pipeline_context().provenance.annotations
    if key in annotations:
        log_manager.get_logger(__name__).warn('Tag `{}` updated to `{}`'.format(key, value))
    annotations[key] = value
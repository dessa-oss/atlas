
# TODO: re-evaluate for jupyter notebooks
def set_project_name(project_name="default"):
    """
    Sets the project a given job. This allows Foundations to know that multiple jobs belong to the same project. The project name is later used to retrieve metrics and analyze experiments

    Arguments:
        project_name {string} -- Optional name specifying which project the job is part of. If no project name is specified, the job will be deployed under the "default" project

    Returns:
        - This function doesn't return a value.

    Raises:
        - This method doesn't raise any exceptions.
    """
    from foundations.global_state import current_foundations_job
    current_foundations_job().project_name = project_name


def _get_metrics_for_all_jobs(project_name):
    """
    Returns metrics for all jobs for a given project.

    Arguments:
        project_name {string} -- Name of the project to filter by.

    Returns:
        metrics {DataFrame} -- A Pandas DataFrame containing all of the results.

    Raises:
        ValueError -- An exception indicating that the requested project does not exist
    """

    from foundations_contrib.models.project_listing import ProjectListing
    from foundations.global_state import redis_connection

    project_info = ProjectListing.find_project(redis_connection, project_name)
    if project_info is None:
        raise ValueError('Project `{}` does not exist!'.format(project_name))

    return _flattened_job_metrics(project_name)


def get_metrics_for_all_jobs(project_name):
    """
    Returns metrics and tags for all jobs for a given project. This function is an experimental feature, and is under the foundations.prototype package

    Arguments:
        project_name {string} -- Name of the project to filter by.

    Returns:
        metrics {DataFrame} -- A Pandas DataFrame containing all of the results.

    Raises:
        ValueError -- An exception indicating that the requested project does not exist
    """
    from foundations_contrib.global_state import redis_connection
    from foundations.helpers.annotate import annotations_for_multiple_jobs
    from pandas import DataFrame

    metrics = _get_metrics_for_all_jobs(project_name)

    if 'job_id' not in metrics:
        return metrics

    metric_rows = list(metrics.T.to_dict().values())

    job_annotations = annotations_for_multiple_jobs(redis_connection, metrics['job_id'])

    for row in metric_rows:
        annotations = job_annotations[row['job_id']]
        for key, value in annotations.items():
            tag_key = 'tag_{}'.format(key)
            row[tag_key] = value

    return DataFrame(metric_rows)


def set_tag(key, value=''):
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
    """
    from foundations.utils import log_warning_if_not_running_in_job
    log_warning_if_not_running_in_job(_set_tag_in_running_jobs, key, value)


def _set_tag_in_running_jobs(key, value):
    from foundations_contrib.global_state import message_router, current_foundations_job
    from foundations_events.producers.tag_set import TagSet

    job_id = current_foundations_job().job_id

    tag_set_producer = TagSet(message_router, job_id, key, value)
    tag_set_producer.push_message()


def _flattened_job_metrics(project_name):
    from pandas import DataFrame, concat

    job_metadata_list = []
    input_params_list = []
    output_metrics_list = []

    for job_data in _project_job_data(project_name):
        _update_job_data(
            job_data,
            input_params_list,
            output_metrics_list
        )
        _update_datetime(job_data)
        job_metadata_list.append(job_data)

    return concat([DataFrame(job_metadata_list), DataFrame(input_params_list), DataFrame(output_metrics_list)], axis=1,
                  sort=False)


def _update_datetime(job_data):
    from foundations.utils import datetime_string

    if 'start_time' in job_data:
        job_data['start_time'] = datetime_string(job_data['start_time'])
    if 'completed_time' in job_data:
        job_data['completed_time'] = datetime_string(
            job_data['completed_time'])


def _update_job_data(job_data, input_param_list, output_metrics_list):
    output_metrics_list.append(job_data['output_metrics'])
    del job_data['output_metrics']
    _shape_input_parameters(job_data, input_param_list)


def _shape_input_parameters(job_data, input_param_list):
    input_param_dict = {}

    input_param_dict.update(job_data['job_parameters'])
    input_param_list.append(input_param_dict)

    del job_data['job_parameters']


def _project_job_data(project_name):
    from foundations_contrib.models.completed_job_data_listing import CompletedJobDataListing
    return CompletedJobDataListing.completed_job_data(project_name)

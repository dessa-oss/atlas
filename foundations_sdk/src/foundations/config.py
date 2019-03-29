"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 03 2019
"""

def set_environment(environment_name):
    """
    Sets the deployment environment where the job is run. Equivalent to specifying --env when deploying through the Foundations CLI

    Arguments:
        environment_name {string} -- the name of the deployment environment. Available environments can be displayed with the Foundations CLI command 'foundations info --env'

    Returns:
        - This function doesn't return a value.

    Raises:
        ValueError -- An exception indicating that the specified environment_name does not exist.

    Notes:
        Primarily used when using Jupyter to specify deployment environment without the Foundations CLI

    Example:
        ```python
        #Jupyter Cell
        import foundations
        foundations.set_environment('local')

        #Jupyter Cell
        from project_code.data_helper import load_data
        from project_code.algorithms import train_model

        load_data = foundations.create_stage(load_data)
        train_model = foundations.create_stage(train_model)
        data = load_data()
        model = train_model(data)
        model.run()
        ```
    """
    from foundations_contrib.global_state import config_manager

    path = _environment_path(environment_name)
    config_manager.add_simple_config_path(path)

def _environment_path(environment_name):
    from foundations_contrib.cli.environment_fetcher import EnvironmentFetcher

    environment_fetcher = EnvironmentFetcher()
    paths = environment_fetcher.find_environment(environment_name)
    if paths:
        return paths[0]
    else:
        raise ValueError(_(environment_name))

def _(environment_name):
    return 'No environment {} found, please set a valid deployment environment with foundations.set_environment'.format(environment_name)

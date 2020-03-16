
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
    """
    from foundations_contrib.global_state import config_manager

    path = _environment_path(environment_name)
    config_manager.add_simple_config_path(path)

def _environment_path(environment_name):
    from foundations_core_cli.environment_fetcher import EnvironmentFetcher

    environment_fetcher = EnvironmentFetcher()
    paths = environment_fetcher.find_environment(environment_name)
    if paths:
        return paths[0]
    else:
        raise ValueError(_(environment_name))

def _(environment_name):
    return 'No environment {} found, please set a valid deployment environment with foundations.set_environment'.format(environment_name)

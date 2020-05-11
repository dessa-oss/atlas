

# import foundations_contrib
import yaml

# with open(f'{foundations_contrib.root()}/resources/config_validation/job.yaml') as file:
#     _job_schema = yaml.load(file.read(), Loader=yaml.FullLoader)

def submit(arguments):
    from foundations_core_cli.job_submission.config import load
    from foundations_core_cli.job_submission.deployment import deploy
    from foundations_core_cli.job_submission.logs import stream_job_logs
    from foundations_internal.change_directory import ChangeDirectory
    from foundations_contrib.global_state import config_manager, log_manager
    from foundations_contrib.set_job_resources import set_job_resources
    from jsonschema import validate
    import os
    import os.path

    current_directory = os.getcwd()
    with ChangeDirectory(arguments.job_directory or current_directory):
        load(arguments.scheduler_config or 'scheduler')

        job_config = {}
        if os.path.exists('job.config.yaml'):
            with open('job.config.yaml') as file:
                job_config = yaml.load(file.read(), Loader=yaml.FullLoader)

        # validate(instance=job_config, schema=_job_schema)

        job_resource_args = {}

        if 'log_level' in job_config:
            config_manager['log_level'] = job_config['log_level']
        if 'worker' in job_config:
            config_manager['worker_container_overrides'].update(job_config['worker'])
        if 'num_gpus' in job_config:
            job_resource_args['num_gpus'] = job_config['num_gpus']
        if 'ram' in job_config:
            job_resource_args['ram'] = job_config['ram']

        logger = log_manager.get_logger(__name__)

        if arguments.command:
            config_manager['worker_container_overrides']['args'] = arguments.command
            if not os.path.exists(arguments.command[0]):
                logger.warning(f"Hey, seems like your command '{arguments.command[0]}' is not an existing file in your current directory. If you are using Atlas's advanced custom docker image functionality and know what you are doing, you can ignore this message.")
        else:
            logger.warning('No command was specified.')

        if arguments.num_gpus is not None:
            job_resource_args['num_gpus'] = arguments.num_gpus
        if arguments.ram is not None:
            job_resource_args['ram'] = arguments.ram
        set_job_resources(**job_resource_args)

        from foundations.global_state import current_foundations_context
        try:
            cur_job_id = current_foundations_context().job_id()
        except ValueError:
            cur_job_id = None

        deployment = deploy(
            arguments.project_name or job_config.get('project_name'),
            arguments.entrypoint or job_config.get('entrypoint'),
            arguments.params or job_config.get('params')
        )

        if arguments.stream_job_logs:
            try:
                stream_job_logs(deployment)
            except KeyboardInterrupt:
                pass

        if cur_job_id is not None:
            current_foundations_context().set_job_id(cur_job_id)

        return deployment
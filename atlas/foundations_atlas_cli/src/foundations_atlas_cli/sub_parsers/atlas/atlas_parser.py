

class AtlasParser(object):
    def __init__(self, commandline):
        self._cli = commandline

    def add_sub_parser(self):
        self._initialize_submit_parser()
        self._initialize_retrieve_parser()
        self._initialize_stop()
        self._initialize_clear_queue()
        self._initialize_delete_parser()

    def _initialize_submit_parser(self):
        from argparse import REMAINDER

        deploy_parser = self._cli.add_sub_parser(
            "submit", help="Deploys a Foundations project to the specified environment"
        )
        deploy_parser.add_argument(
            "--entrypoint",
            type=str,
            help="Command process will execute with (default: python)",
        )
        deploy_parser.add_argument(
            "--project-name",
            help="Project name for job (default: base name of cwd directory)",
        )
        deploy_parser.add_argument(
            "--num-gpus",
            type=int,
            help="A non-zero value will run a GPU-enabled job with all available GPUs. Does not currently support allocate GPU quantity (default: 0)",
        )
        deploy_parser.add_argument(
            "--ram",
            type=float,
            help="GB of RAM to allocate for job (default: no limit)",
        )
        deploy_parser.add_argument(
            "--stream-job-logs",
            type=self._str_to_bool,
            default=True,
            help="Whether or not to stream job logs (default: True)",
        )
        deploy_parser.add_argument(
            "scheduler_config",
            metavar="scheduler-config",
            help="Environment to run file in",
        )
        deploy_parser.add_argument(
            "job_directory",
            type=str,
            metavar="job-directory",
            help="Directory from which to deploy",
        )
        deploy_parser.add_argument(
            "command",
            type=str,
            nargs=REMAINDER,
            help="Arguments to be used by the entrypoint",
        )
        deploy_parser.set_defaults(function=self._submit)
        deploy_parser.set_defaults(params={})

    def _initialize_retrieve_parser(self):
        retrieve_parser = self._cli.add_sub_parser(
            "get", help="Get file types from execution environments"
        )
        retrieve_subparsers = retrieve_parser.add_subparsers()
        self._initialize_retrieve_artifact_parser(retrieve_subparsers)
        self._initialize_retrieve_logs_parser(retrieve_subparsers)

    def _initialize_retrieve_artifact_parser(self, retrieve_subparsers):
        retrieve_artifact_parser = retrieve_subparsers.add_parser(
            "job", help="Specify job to retrieve artifacts from"
        )
        retrieve_artifact_parser.add_argument(
            "scheduler_config", type=str, help="Environment to get from"
        )
        retrieve_artifact_parser.add_argument(
            "job_id", type=str, help="Specify job uuid of already deployed job"
        )
        retrieve_artifact_parser.add_argument(
            "--save_dir",
            type=str,
            default=None,
            help="Specify local directory path for artifacts to save to. Defaults to directory within current working directory",
        )
        retrieve_artifact_parser.add_argument(
            "--source_dir",
            type=str,
            default="",
            help="Specify relative directory path to download artifacts from. Default will download all artifacts from job",
        )
        retrieve_artifact_parser.set_defaults(function=self._retrieve_artifacts)

    def _initialize_retrieve_logs_parser(self, retrieve_subparsers):
        retrieve_logs_parser = retrieve_subparsers.add_parser(
            "logs", help="Get logs for jobs"
        )
        retrieve_logs_parser.add_argument(
            "scheduler_config", type=str, help="Environment to get from"
        )
        retrieve_logs_parser.add_argument(
            "job_id", type=str, help="Specify job uuid of already deployed job"
        )
        retrieve_logs_parser.set_defaults(function=self._retrieve_logs)

    def _initialize_stop(self):
        stop_parser = self._cli.add_sub_parser("stop", help="Stops a running job")
        stop_parser.add_argument(
            "scheduler_config",
            metavar="scheduler-config",
            help="Environment the job is running in",
        )
        stop_parser.add_argument(
            "job_id", type=str, help="Specify job ID of running job"
        )
        stop_parser.set_defaults(function=self._stop)

    def _initialize_clear_queue(self):
        clear_queue_parser = self._cli.add_sub_parser(
            "clear-queue", help="Clears all scheduled jobs from the queue"
        )
        clear_queue_parser.add_argument(
            "scheduler_config",
            metavar="scheduler-config",
            help="Environment to clear the queue",
        )
        clear_queue_parser.set_defaults(function=self._clear_queue)

    def _initialize_delete_parser(self):
        delete_parser = self._cli.add_sub_parser(
            "delete", help="Delete items from execution environment"
        )
        delete_subparsers = delete_parser.add_subparsers()
        self._initialize_delete_job_parser(delete_subparsers)

    def _initialize_delete_job_parser(self, delete_subparsers):
        delete_job_parser = delete_subparsers.add_parser("job", help="Delete jobs")
        delete_job_parser.add_argument(
            "scheduler_config", type=str, help="Environment to delete job from"
        )
        delete_job_parser.add_argument(
            "job_id", type=str, help="Specify job ID of already deployed job"
        )
        delete_job_parser.set_defaults(function=self._delete_job)

    def _submit(self):
        from foundations_core_cli.job_submission.submit_job import submit

        submit(self._cli.arguments())

    def _retrieve_artifacts(self):
        from foundations_contrib.global_state import config_manager
        from foundations_core_cli.job_submission.config import load
        from foundations_internal.change_directory import ChangeDirectory
        import os

        arguments = self._cli.arguments()

        env_name = arguments.scheduler_config
        job_id = arguments.job_id
        current_directory = os.getcwd()

        if arguments.save_dir is None:
            arguments.save_dir = os.path.join(current_directory, str(job_id))

        with ChangeDirectory(current_directory):
            load(arguments.scheduler_config or "scheduler")

        job_deployment_class = config_manager["deployment_implementation"][
            "deployment_type"
        ]
        job_deployment = job_deployment_class(job_id, None, None)

        job_status = job_deployment.get_job_status()

        if job_status is None:
            self._cli._fail_with_message(
                "Error: Job `{}` does not exist for environment `{}`".format(
                    job_id, env_name
                )
            )
        else:
            if job_deployment.get_job_archive():
                print(f"Successfully retrieved Job {job_id} from archive store")
            else:
                print(f"Error: Could not download Job {job_id}")

    def _retrieve_logs(self):
        from foundations_contrib.global_state import config_manager
        from foundations_core_cli.job_submission.config import load
        from foundations_internal.change_directory import ChangeDirectory
        import os

        arguments = self._cli.arguments()

        env_name = arguments.scheduler_config
        job_id = arguments.job_id
        current_directory = os.getcwd()

        with ChangeDirectory(current_directory):
            load(arguments.scheduler_config or "scheduler")

        job_deployment_class = config_manager["deployment_implementation"][
            "deployment_type"
        ]
        job_deployment = job_deployment_class(job_id, None, None)

        job_status = job_deployment.get_job_status()

        if job_status is None:
            self._cli._fail_with_message(
                "Error: Job `{}` does not exist for environment `{}`".format(
                    job_id, env_name
                )
            )
        elif job_status == "queued":
            self._cli._fail_with_message(
                "Error: Job `{}` is queued and has not produced any logs".format(job_id)
            )
        else:
            logs = job_deployment.get_job_logs()
            print(logs)

    def _stop(self):
        from foundations_contrib.global_state import config_manager
        from foundations_core_cli.job_submission.config import load
        from foundations_internal.change_directory import ChangeDirectory
        import os

        arguments = self._cli.arguments()

        env_name = arguments.scheduler_config
        job_id = arguments.job_id
        current_directory = os.getcwd()

        with ChangeDirectory(current_directory):
            load(arguments.scheduler_config or "scheduler")

        job_deployment_class = config_manager["deployment_implementation"][
            "deployment_type"
        ]
        job_deployment = job_deployment_class(job_id, None, None)

        try:
            job_status = job_deployment.get_job_status()

            if job_status is None:
                self._cli._fail_with_message(
                    "Error: Job `{}` does not exist for environment `{}`".format(
                        job_id, env_name
                    )
                )
            elif job_status == "queued":
                self._cli._fail_with_message(
                    "Error: Job `{}` is queued and cannot be stopped".format(job_id)
                )
            elif job_status == "completed":
                self._cli._fail_with_message(
                    "Error: Job `{}` is completed and cannot be stopped".format(job_id)
                )
            else:
                if job_deployment.stop_running_job():
                    print("Stopped running job {}".format(job_id))
                else:
                    print("Error stopping job {}".format(job_id))
        except AttributeError:
            print("The specified scheduler does not support this functionality")

    def _clear_queue(self):
        from foundations_contrib.global_state import config_manager
        from foundations_core_cli.job_submission.config import load
        from foundations_internal.change_directory import ChangeDirectory
        import os

        arguments = self._cli.arguments()

        current_directory = os.getcwd()

        with ChangeDirectory(current_directory):
            load(arguments.scheduler_config or "scheduler")

        job_deployment_class = config_manager["deployment_implementation"][
            "deployment_type"
        ]

        try:
            num_jobs_dequeued = job_deployment_class.clear_queue()
            print("Removed {} job(s) from queue".format(num_jobs_dequeued))
        except AttributeError:
            print("The specified scheduler does not support this functionality")

    def _delete_job(self):
        from foundations_contrib.global_state import config_manager
        from foundations_core_cli.job_submission.config import load
        from foundations_internal.change_directory import ChangeDirectory
        import os

        arguments = self._cli.arguments()

        env_name = arguments.scheduler_config
        job_id = arguments.job_id
        current_directory = os.getcwd()

        with ChangeDirectory(current_directory):
            load(arguments.scheduler_config or "scheduler")

        job_deployment_class = config_manager["deployment_implementation"][
            "deployment_type"
        ]
        job_deployment = job_deployment_class(job_id, None, None)

        job_status = job_deployment.get_job_status()

        if job_status is None:
            self._cli._fail_with_message(
                "Error: Job `{}` does not exist for environment `{}`".format(
                    job_id, env_name
                )
            )
        elif job_status in ("queued", "running", "pending"):
            self._cli._fail_with_message(
                "Error: Job `{}` has status `{}` and cannot be deleted".format(
                    job_id, job_status
                )
            )
        else:
            if job_deployment.cancel_jobs([job_id])[job_id]:
                print(f"Job {job_id} successfully deleted")
            else:
                print(
                    f"Could not completely delete job {job_id}. Please make sure that the job bundle exists under ~/.foundations/job_data/"
                )

    @staticmethod
    def _str_to_bool(string_value):
        return string_value == "True"

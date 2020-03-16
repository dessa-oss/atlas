import sys


class CommandLineInterface(object):
    def __init__(self, args):
        self._input_arguments = args

        self._argument_parser = self._initialize_argument_parser()
        self._subparsers = self._argument_parser.add_subparsers()

        try:
            from foundations_atlas_cli.sub_parsers.atlas.atlas_parser import AtlasParser

            AtlasParser(self).add_sub_parser()
        except ModuleNotFoundError:
            pass

        self._initialize_init_parser()
        self._initialize_info_parser()
        self._initialize_login_parser()

    def add_sub_parser(self, name, help=None):
        sub_parser = self._subparsers.add_parser(name, help=help)
        sub_parser.add_argument(
            "--debug", action="store_true", help="Sets debug mode for the CLI"
        )
        return sub_parser

    def _initialize_argument_parser(self):
        from argparse import ArgumentParser

        argument_parser = ArgumentParser(prog="foundations")
        argument_parser.add_argument(
            "--version",
            action="store_true",
            help="Displays the current Foundations version",
        )
        argument_parser.add_argument(
            "--debug", action="store_true", help="Sets debug mode for the CLI"
        )
        argument_parser.set_defaults(function=self._no_command)
        return argument_parser

    def _initialize_init_parser(self):
        init_parser = self.add_sub_parser(
            "init", help="Creates a new Foundations project in the current directory"
        )
        init_parser.add_argument(
            "project_name", type=str, help="Name of the project to create"
        )
        init_parser.set_defaults(function=self._init)

    @staticmethod
    def _str_to_bool(string_value):
        return string_value == "True"

    def _initialize_info_parser(self):
        info_parser = self.add_sub_parser(
            "info", help="Provides information about your Foundations project"
        )
        info_parser.add_argument("--env", action="store_true")
        info_parser.set_defaults(function=self._info)

    def _initialize_login_parser(self):
        import sys

        login_parser = self.add_sub_parser(
            "login", help="Login to an Atlas cluster"
        )
        login_parser.add_argument(
            "host",
            help="The address of the instance to login to (e.g. http://0.0.0.0:3333)",
        )
        login_parser.add_argument(
            "-u", "--username", required=False, type=str, help="Username as plain text"
        )
        login_parser.add_argument(
            "-p",
            "--password",
            type=str,
            required="--username" in sys.argv,
            help="Password in plain text",
        )
        login_parser.set_defaults(function=self._login)

    def execute(self):
        self._arguments = self._argument_parser.parse_args(self._input_arguments)
        try:
            self._arguments.function()
        except Exception as error:
            if self._arguments.debug == True:
                raise
            print(f"Error running command: {error}")
            sys.exit(1)

    def arguments(self):
        return self._arguments

    def _no_command(self):
        import foundations

        if self._arguments.version:
            print("Running Foundations version {}".format(foundations.__version__))
        else:
            self._argument_parser.print_help()

    def _init(self):
        from foundations_core_cli.scaffold import Scaffold

        project_name = self._arguments.project_name
        result = Scaffold(project_name).scaffold_project()
        if result:
            print("Success: New Foundations project `{}` created!".format(project_name))
        else:
            print(
                "Error: project directory for `{}` already exists".format(project_name)
            )

    def _info(self):
        from foundations_core_cli.environment_fetcher import EnvironmentFetcher

        env_name = self._arguments.env

        if not env_name:
            print("usage: foundations info [--env ENV]")
            return

        (
            project_environment,
            global_environment,
        ) = EnvironmentFetcher().get_all_environments()

        if len(global_environment) == 0 and (
            project_environment == None or len(project_environment) == 0
        ):
            print("No environments available")
        else:
            self._print_configs("submission", global_environment)
            if project_environment != None:
                self._print_configs("execution", project_environment)

    def _login(self):
        import getpass
        import requests
        from os.path import expanduser, join
        import yaml
        from foundations_contrib.utils import foundations_home

        username = self._arguments.username
        password = self._arguments.password

        if username is None or password is None:
            username = input("Username: ")
            password = getpass.getpass(prompt="Password: ", stream=False)

        resp = requests.get(
            f"{self._arguments.host}/api/v2beta/auth/cli_login",
            auth=(username, password),
        )
        if resp.status_code == 200:
            credential_filepath = expanduser(
                join(foundations_home(), "credentials.yaml")
            )
            with open(credential_filepath, "w") as creds_file:
                creds = {"default": {"token": resp.json()["access_token"]}}
                yaml.dump(creds, creds_file, default_flow_style=False)
            print("\nLogin Succeeded!")
        else:
            print("\nLogin Failed!")
            print(f"Error response: {resp.text}")

    def _print_configs(self, config_list_name, config_list):
        config_list = self._create_environment_list(config_list)
        print("\n{} configs:".format(config_list_name))
        if len(config_list) == 0:
            print("No {} environments available".format(config_list_name))
        else:
            print(self._format_environment_printout(config_list))

    def _format_environment_printout(self, environment_array):
        from tabulate import tabulate

        return tabulate(environment_array, headers=["env_name", "env_path"])

    def _create_environment_list(self, available_environments):
        import os

        environment_names = []
        for env in available_environments:
            environment_names.append([env.split(os.path.sep)[-1].split(".")[0], env])
        return environment_names

    def _load_configuration(self):
        from foundations_core_cli.environment_fetcher import EnvironmentFetcher
        from foundations_contrib.global_state import config_manager

        env_name = self._arguments.env
        env_file_path = EnvironmentFetcher().find_environment(env_name)

        if env_file_path and env_file_path[0]:
            config_manager.add_simple_config_path(env_file_path[0])
        else:
            self._fail_with_message(
                "Error: Could not find environment `{}`".format(env_name)
            )

    def _fail_with_message(self, message):
        import sys

        print(message)
        sys.exit(1)


# separates test runs
from uuid import uuid4

TEST_UUID = uuid4()


def set_foundations_home():
    import os

    os.environ["FOUNDATIONS_HOME"] = os.getcwd() + "/auth_acceptance/foundations_home"
    os.environ["FOUNDATIONS_COMMAND_LINE"] = "True"


def _flattened_config_walk():
    import os
    import os.path as path

    for dir_name, _, files in os.walk("auth_acceptance/foundations_home"):
        for file_name in files:
            if file_name.endswith(".envsubst.yaml"):
                yield path.join(dir_name, file_name)


def _load_execution_config():
    from foundations_core_cli.typed_config_listing import TypedConfigListing
    from foundations_internal.config.execution import translate

    TypedConfigListing("execution").update_config_manager_with_config(
        "default", translate
    )


def _config():
    import os
    import subprocess

    for env_var in ["FOUNDATIONS_HOME"]:
        if not os.environ.get(env_var, None):
            print(f"{env_var} was not set")
            exit(1)

    for template_file_name in _flattened_config_walk():
        output_file_name = template_file_name[: -len(".envsubst.yaml")] + ".yaml"
        subprocess.run(
            f"envsubst < {template_file_name} > {output_file_name}", shell=True
        )

    # _load_execution_config()


def setup_auth_home_config():
    set_foundations_home()
    _config()

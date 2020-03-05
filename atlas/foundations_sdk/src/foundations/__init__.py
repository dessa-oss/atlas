

def _check_if_in_cli():
    import traceback
    import os
    import os.path

    in_run_py = False
    in_unit_test = False
    for line in traceback.format_stack():
        if "runpy.py" in line:
            in_run_py = True
        elif "unittest" in line:
            in_unit_test = True

    if in_run_py and not in_unit_test:
        os.environ["FOUNDATIONS_COMMAND_LINE"] = "True"


_check_if_in_cli()

from foundations.global_state import *
from foundations_contrib.bucket_pipeline_archive import BucketPipelineArchive
from foundations_contrib.bucket_pipeline_listing import BucketPipelineListing
from foundations_contrib.prefixed_bucket import PrefixedBucket
from foundations_internal.serializer import *
from foundations_internal.change_directory import ChangeDirectory
from foundations_contrib.bucket_job_deployment import BucketJobDeployment
from foundations_contrib.archiving.save_artifact import save_artifact
from foundations_contrib.deployment_wrapper import DeploymentWrapper
from foundations.projects import set_project_name, set_tag, get_metrics_for_all_jobs
from foundations_internal.versioning import __version__
from foundations.config import set_environment
from foundations.job_parameters import *
from foundations.job_metrics import *
import foundations_events.consumers
import foundations_events
from foundations_contrib.set_job_resources import set_job_resources
from foundations.submission import *
import foundations_core_cli

from foundations.artifacts import *
from foundations.local_run import set_up_default_environment_if_present


def _append_module():
    import sys
    from foundations_internal.global_state import module_manager

    module_manager.append_module(sys.modules[__name__])


_append_module()

set_up_default_environment_if_present()
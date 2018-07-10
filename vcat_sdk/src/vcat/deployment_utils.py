"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def gcp_deploy_job(job, job_name):
    from vcat.job_source_bundle import JobSourceBundle
    from vcat.gcp_job_deployment import GCPJobDeployment
    from uuid import uuid4

    bundle_name = str(uuid4())
    job_source_bundle = JobSourceBundle(bundle_name, '../')
    deployment = GCPJobDeployment(job_name, job, job_source_bundle)
    deployment.deploy()
    return deployment

def extract_results(fetched_results):
    results = {}

    for stage_context in fetched_results["stage_contexts"].values():
        stage_log_entry = stage_context["stage_log"]
        results.update(stage_log_entry)

    return results

def wait_on_deployment_set(deployment_set, time_to_sleep=5, error_handler=None):
    import time

    from vcat.global_state import log_manager

    log = log_manager.get_logger(__name__)

    while deployment_set != {}:
        _collect_results_and_remove_finished_deployments(deployment_set, error_handler)
        time.sleep(time_to_sleep)

    log.info('All deployments completed.')
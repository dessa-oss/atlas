"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def gcp_deploy_job(job, job_name):
    from foundations.job_source_bundle import JobSourceBundle
    from foundations.gcp_job_deployment import GCPJobDeployment
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

def _grab_and_log_results(logger, deployment, error_handler):
    logged_results = deployment._try_get_results(error_handler)
    logger.info(deployment.job_name() + ": " + str(logged_results))
    return logged_results

def collect_results_and_remove_finished_deployments(logger, deployment_set, error_handler):
    from foundations.utils import _remove_items_by_key

    jobs_done = []
    all_logged_results = []

    for job_name, deployment in deployment_set.items():
        logger.info(job_name + ": " + deployment.get_job_status())

        if deployment.is_job_complete():
            logged_results = _grab_and_log_results(logger, deployment, error_handler)
            jobs_done.append(deployment.job_name())
            all_logged_results.append(logged_results)

    _remove_items_by_key(deployment_set, jobs_done)

    logger.info("----------\n")

    return all_logged_results

def wait_on_deployment_set(deployment_set, time_to_sleep=5, error_handler=None):
    import time

    from foundations.global_state import log_manager

    log = log_manager.get_logger(__name__)

    while deployment_set != {}:
        collect_results_and_remove_finished_deployments(log, deployment_set, error_handler)
        time.sleep(time_to_sleep)

    log.info('All deployments completed.')
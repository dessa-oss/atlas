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

def wait_on_deployments_map(deployments_map, time_to_sleep=5):
    import time

    from vcat.global_state import log_manager

    log = log_manager.get_logger(__name__)

    while deployments_map != {}:
        jobs_done = []

        for job_name, deployment in deployments_map.items():
            job_status = deployment.get_job_status()

            log.info(job_name + ": " + job_status)

            if deployment.is_job_complete():
                log.info(job_name + ": " + str(deployment.fetch_job_results()))
                jobs_done.append(job_name)

        for job_name in jobs_done:
            deployments_map.pop(job_name)

        log.info("----------\n")

        time.sleep(time_to_sleep)
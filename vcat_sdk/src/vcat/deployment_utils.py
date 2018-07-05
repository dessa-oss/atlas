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

def _grid_param_set_generator(hype_kwargs):
    import itertools

    hype_dict = {}

    for key, val in hype_kwargs.items():
        if isinstance(val, list):
            hype_dict[key] = val
        else:
            hype_dict[key] = [val]

    param_keys = []
    param_vals_to_select = []

    for key, val in hype_dict.items():
        param_keys.append(key)
        param_vals_to_select.append(val)

    for param_vals in itertools.product(*param_vals_to_select):
        param_set_entry = {}

        for param_key, param_val in zip(param_keys, param_vals):
            param_set_entry[param_key] = param_val

        yield param_set_entry


def _extract_results(results_dict):
    results = {}

    for result_entry in results_dict["results"].values():
        results.update(result_entry)

    return results
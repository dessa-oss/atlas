"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def get_results_list(deployments):
    from foundations.deployment_utils import extract_results

    all_results = []
    for deployment in deployments.values():
        results = deployment.fetch_job_results()
        results = extract_results(results)
        all_results.append(results)

    return all_results

def get_sorted_results_items_list(deployments):
    return make_list_of_dicts_comparable(get_results_list(deployments))

def p_items(*args):
    p0, p1, p2 = args[0]

    return [
        ('param_0', p0),
        ('param_1', p1),
        ('param_2', p2)
    ]

def params_cart_prod(*params_lists):
    import itertools

    cart_prod = itertools.product(*params_lists)
    mapped = map(p_items, cart_prod)

    return list(mapped)

def make_list_of_dicts_comparable(list_of_dicts):
    to_return = []

    for dict_obj in list_of_dicts:
        entry = list(dict_obj.items())
        entry.sort()
        to_return.append(entry)

    to_return.sort()

    return to_return

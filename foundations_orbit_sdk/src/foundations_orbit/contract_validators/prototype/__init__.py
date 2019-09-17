"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import numpy as np
import pickle

from .utils import nand, bin_values, count_and_remove_special_values, bin_current_values, add_special_value_l_infinity, \
    add_binned_l_infinity

from foundations_contrib.global_state import redis_connection

def create_bin_stats(special_values, max_bins, col_values):
    bin_dicts = []
    n_vals = len(col_values)
    # for every special value, make a bin for it
    for sv in special_values:
        sv_count = len(col_values[col_values == sv])
        sv_dict = {'value': sv, "percentage": sv_count/n_vals}
        # drop current special value
        col_values = col_values[col_values != sv]
        bin_dicts.append(sv_dict)
    # make bins for all non-special values
    bin_counts, bin_edges = bin_values(col_values, max_bins)
    bin_percentages = list(np.array(bin_counts)/n_vals)
    # case: there is only one unique value
    if len(bin_edges) == 0:
        unique_value = col_values[0]
        bin_dicts.append({'value': unique_value, 'percentage': len(col_values)/n_vals,
                            'upper_edge': None})
    # otherwise there is more than one unique value
    else:
        bin_edges.append(np.inf)
        for i, pct in enumerate(bin_percentages):
            bin_dict = {"percentage": pct, "upper_edge": bin_edges[i]}
            bin_dicts.append(bin_dict)
    return bin_dicts

def distribution_check(config_dict, column_names, bin_stats, current_df):
    '''
        Expected format of dist_check_results
        {'col1': {'binned_passed': False,
                'binned_l_infinity': 0.2,
                'special_values':
                    {'nan':
                        {'percentage_diff': 0.15, 'ref_percentage': 0, 'current_percentage': 0.15, 'passed': True}
                    }
                }
    :param ref_col_stats:
    :param current_df:
    :return:
    '''
    dist_check_results = {}
    # get the list of columns to check
    dist_check_config = config_dict
    cols_to_check = set(current_df.columns).intersection(set(column_names))
    # only one of cols_to_check and cols_to_ignore can be non-None
    assert nand(dist_check_config['cols_to_include'] is not None, dist_check_config['cols_to_ignore'] is not None)
    
    if dist_check_config['cols_to_include'] is not None:
        cols_to_check = set(dist_check_config['cols_to_include']).intersection(cols_to_check)
    elif dist_check_config['cols_to_ignore'] is not None:
        cols_to_check = cols_to_check - set(dist_check_config['cols_to_ignore'])

    # apply check to each col in cols_to_check
    cols_to_check = [col for col in current_df.columns if col in cols_to_check] # use same order as current_df

    # for each column extract relevant information (bin stats + special values)
    for col in cols_to_check:
        current_values = current_df[col].copy()
        n_current_vals = len(current_values)
        dist_check_results[col] = {}
        # bin the col in current_df using edges from reference
        ref_special_value_percentages = []
        ref_bin_percentages = []
        ref_special_values = []
        ref_edges = []
        unique_ref_value = None
        ref_bin_stats = bin_stats[col]
        for bin in ref_bin_stats:
            # special value
            if 'upper_edge' not in bin:
                ref_special_values.append(bin['value'])
                ref_special_value_percentages.append(bin['percentage'])
            # unique value
            elif 'upper_edge' in bin and bin['upper_edge'] is None:
                unique_ref_value = bin['value']
                ref_bin_percentages.append(bin['percentage'])
                ref_bin_percentages.append(0)  # to compare with current_other_value_counts percentage
            # normal bins
            else:
                ref_bin_percentages.append(bin['percentage'])
                # the upper_edge of the bin with the largest values is np.inf, ref_edges shouldn't include this
                if bin['upper_edge'] != np.inf:
                    ref_edges.append(bin['upper_edge'])

        # accounting for special values
        current_values, current_special_value_percentages = count_and_remove_special_values(ref_special_values, current_values)

        # binning current_values
        current_bin_percentages = bin_current_values(current_values, ref_edges, n_current_vals, unique_ref_value)

        # define threshold for l_infinity tests
        custom_threshold = dist_check_config['custom_thresholds'].get(col, None)
        threshold = custom_threshold if custom_threshold != None else dist_check_config['default_threshold']

        # add l_infinity test results to dist_check_results
        add_special_value_l_infinity(col, threshold, dist_check_results, ref_special_values,
                                        ref_special_value_percentages, current_special_value_percentages)

        # add l_infinity test results to dist_check_results
        add_binned_l_infinity(col, threshold, dist_check_results, ref_bin_percentages, current_bin_percentages)

    return dist_check_results

# deprecated (functionality replaces by the ReportFormatter) code to be removed
def output_for_writing(
    corresponding_date,
    model_package_name,
    contract_name,
    row_cnt_diff,
    schema_check_passed_flag,
    n_ref_cols,
    schema_check_failure_dict,
    n_current_cols,
    current_df_dtype_mapping,
    reference_df_type_mapping,
    distribution_check_flag,
    dist_check_results,
    special_values
    ):

    output_dict = {}
    output_dict['date'] = str(corresponding_date)
    output_dict['model_package'] = model_package_name
    output_dict['data_contract'] = contract_name
    output_dict['row_cnt_diff'] = row_cnt_diff
    if schema_check_passed_flag:
        output_dict['schema'] = {'summary': {'healthy': n_ref_cols,
                                                'critical': 0}
                                    }
    else:
        schema_error_message = schema_check_failure_dict['error_message']
        output_dict["details_by_attribute"] = list()
        details_by_attribute = output_dict["details_by_attribute"]
        if schema_error_message == 'column sets not equal':
            missing_in_ref = schema_check_failure_dict['missing_in_ref']
            missing_in_current = schema_check_failure_dict['missing_in_current']
            n_error_state = len(missing_in_ref) + len(missing_in_current)
            n_healthy = n_current_cols - len(missing_in_ref)
            output_dict['schema'] = {'summary': {'healthy': n_healthy,
                                                    'critical': n_error_state}}
            # details by attribute
            for col in missing_in_ref:
                col_dict = {}
                col_dict["attribute_name"] = col
                col_dict["data_type"] = str(current_df_dtype_mapping[col])
                col_dict["issue_type"] = "missing in reference"
                col_dict["validation_outcome"] = "error_state"
                details_by_attribute.append(col_dict)

            for col in missing_in_current:
                col_dict = {}
                col_dict["attribute_name"] = col
                col_dict["data_type"] = np.nan
                col_dict["issue_type"] = "missing in current dataframe"
                col_dict["validation_outcome"] = "error_state"
                details_by_attribute.append(col_dict)

        elif schema_error_message == 'columns not in order':
            n_unhealthy = len(schema_check_failure_dict['columns_out_of_order'])
            output_dict['schema'] = {'summary': {'healthy': n_current_cols - n_unhealthy,
                                                    'critical': n_unhealthy}}
            # details by attribute
            for col in schema_check_failure_dict['columns_out_of_order']:
                col_dict = {}
                col_dict["attribute_name"] = col
                col_dict["data_type"] = str(current_df_dtype_mapping[col])
                col_dict["issue_type"] = "column is out of order"
                col_dict["validation_outcome"] = "error_state"
                details_by_attribute.append(col_dict)

        elif schema_error_message == 'column datatype mismatches':
            n_unhealthy = len(schema_check_failure_dict['cols'])
            output_dict['schema'] = {'summary': {'healthy': n_current_cols - n_unhealthy,
                                                    'critical': n_unhealthy}}
            # details by attribute
            for col in schema_check_failure_dict['cols']:
                col_dict = {}
                col_dict["attribute_name"] = col
                col_dict["data_type"] = str(current_df_dtype_mapping[col])
                col_dict["issue_type"] = f"datatype in reference is {reference_df_type_mapping[col]}"
                col_dict["validation_outcome"] = "error_state"
                details_by_attribute.append(col_dict)

    if distribution_check_flag:
        output_data_quality = dict()
        output_population_shift = dict()

        data_quality_summary = {'critical': 0, 'healthy': 0}
        population_shift_summary = {'critical': 0, 'healthy': 0}
        data_quality_attribute_details = []
        population_shift_attribute_details = []

        for col in dist_check_results:
            col_results = dist_check_results[col]
            # for each special value
            for sv in special_values:
                sv_dict = col_results['special_values'][sv]
                # make data quality / special value attribute details
                attribute_details = dict()
                attribute_details["attribute_name"] = col
                attribute_details["value"] = str(sv)
                attribute_details["pct_in_reference_data"] = sv_dict['ref_percentage']
                attribute_details["pct_in_current_data"] = sv_dict['current_percentage']
                attribute_details["difference_in_pct"] = sv_dict['percentage_diff']
                attribute_details["validation_outcome"] = "healthy" if sv_dict["passed"] else "critical"
                data_quality_attribute_details.append(attribute_details)
                if sv_dict["passed"]:
                    data_quality_summary['healthy'] += 1
                else:
                    data_quality_summary['critical'] += 1

            # make distribution shift (all the normal bins) json
            attribute_details = dict()
            attribute_details["attribute_name"] = col
            attribute_details["L-infinity"] = col_results["binned_l_infinity"]
            attribute_details["validation_outcome"] = "healthy" if col_results["binned_passed"] else "critical"
            population_shift_attribute_details.append(attribute_details)
            if col_results["binned_passed"]:
                population_shift_summary['healthy'] += 1
            else:
                population_shift_summary['critical'] += 1

        # add results to json
        output_data_quality["details_by_attribute"] = data_quality_attribute_details
        output_data_quality["summary"] = data_quality_summary
        output_population_shift["details_by_attribute"] = population_shift_attribute_details
        output_population_shift["summary"] = population_shift_summary
        output_dict["data_quality"] = output_data_quality
        output_dict["population_shift"] = output_population_shift

    return pickle.dumps(output_dict)

def write_to_redis(project_name, model_name, contract_name, inference_period, serialized_output):
    key = f'projects:{project_name}:models:{model_name}:validation:{contract_name}'
    redis_connection.hset(key, inference_period, serialized_output)
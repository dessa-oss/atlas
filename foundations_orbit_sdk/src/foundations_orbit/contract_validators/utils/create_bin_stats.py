"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import numpy as np
from foundations_orbit.contract_validators.prototype.utils import nand, bin_values

def create_bin_stats(special_values, max_bins, col_values):
    bin_dicts = []
    n_vals = len(col_values)
    if n_vals < 1:
        raise ValueError('Invalid Column Values: Cannot create bin stats for empty column')

    if not isinstance(max_bins, int):
        raise ValueError('Invalid Max Bin: Max bin must be defined as an integer')

    if max_bins < 1:
        raise ValueError('Invalid Max Bin: Cannot create bin stats with bins less than 1.')
    # for every special value, make a bin for it
    for sv in special_values:
        sv_count = len(col_values[col_values == sv])
        sv_dict = {'value': sv, "percentage": sv_count/n_vals}
        # drop current special value
        col_values = col_values[col_values != sv]
        bin_dicts.append(sv_dict)

    if len(col_values) > 0:
        # make bins for all non-special values
        bin_counts, bin_edges = bin_values(col_values, max_bins)
        bin_percentages = list(np.array(bin_counts)/n_vals)
        # case: there is only one unique value
        if len(bin_edges) == 0:
            unique_value = col_values.iloc[0]
            bin_dicts.append({
                'value': unique_value,
                'percentage': len(col_values)/n_vals,
                'upper_edge': None
            })
        # otherwise there is more than one unique value
        else:
            bin_edges.append(np.inf)
            for i, pct in enumerate(bin_percentages):
                bin_dict = {
                    "percentage": pct,
                    "upper_edge": bin_edges[i]
                }
                bin_dicts.append(bin_dict)

    return bin_dicts
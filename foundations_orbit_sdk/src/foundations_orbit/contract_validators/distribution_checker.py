"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class DistributionChecker(object):
    
    def __init__(self, distribution_options):
        self._distribution_options = distribution_options

    def distribution_check_results(self, columns_to_validate):
        import numpy

        if self._distribution_options['cols_to_include'] is not None and self._distribution_options['cols_to_ignore'] is not None:
            raise ValueError('cannot set both cols_to_ignore and cols_to_include - user may set at most one of these attributes')

        dist_check_results = {}

        results_for_same_distribution = {
            'binned_l_infinity': 0.0,
            'binned_passed': True,
            'special_values': {
                numpy.nan: {
                    'current_percentage': 0.0,
                    'passed': True,
                    'percentage_diff': 0.0,
                    'ref_percentage': 0.0
                }
            }
        }

        for column_name in columns_to_validate:
            dist_check_results[column_name] = results_for_same_distribution

        return dist_check_results
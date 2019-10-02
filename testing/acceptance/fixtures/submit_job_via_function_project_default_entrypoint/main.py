"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import foundations
import json

params = foundations.load_parameters()
foundations.log_metric('how_i_lern', params['learning_rate'])
foundations.log_metric('first_boi', params['layers'][0]['neurons'])
foundations.log_metric('second_boi', params['layers'][1]['neurons'])
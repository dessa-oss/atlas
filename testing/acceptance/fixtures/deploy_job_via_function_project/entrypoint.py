"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import foundations
import json

params = foundations.load_parameters()
foundations.log_metric('learning_rate', params['learning_rate'])
foundations.log_metric('layer_0_neuron', params['layers'][0]['neurons'])
foundations.log_metric('layer_1_neuron', params['layers'][1]['neurons'])
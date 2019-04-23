"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""

def log_predictions_for_assertion(preprocessed_data):
    foundations.log_metric('preprocessed_data_sex', list(preprocessed_data['Sex']))
    foundations.log_metric('preprocessed_data_cabin', list(preprocessed_data['Cabin']))
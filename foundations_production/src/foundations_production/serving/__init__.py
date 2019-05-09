"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""

def create_retraining_job(model_package_id, features_location, targets_location):
    from foundations_production.serving.data_from_file import data_from_file
    import foundations

    def dummy_function():
        pass

    data_from_file(features_location)
    return foundations.create_stage(dummy_function)()
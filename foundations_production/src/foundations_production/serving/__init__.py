"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""

def create_retraining_job(model_package_id, features_location, targets_location):
    preparation_stage = _prepare_job_workspace(model_package_id)
    model_package = _model_package_for_retraining(preparation_stage, model_package_id)
    features, targets = _data_for_retraining(features_location, targets_location)
    preprocessed_features = _preprocessed_features(model_package, features)
    return _retrained_model(model_package, preprocessed_features, targets)

def _prepare_job_workspace(model_package_id):
    import os
    import sys
    from foundations_production.serving import create_job_workspace

    workspace_path = '/tmp/foundations_workspaces/{}'.format(model_package_id)

    create_job_workspace(model_package_id)
    os.chdir(workspace_path)
    sys.path.append(workspace_path)

def _retrained_model(model_package, preprocessed_features, targets):    
    production_model = model_package.model
    return production_model.retrain(preprocessed_features, targets, None, None)

def _preprocessed_features(model_package, features):    
    preprocessor = model_package.preprocessor
    return preprocessor(features)

def _data_for_retraining(features_location, targets_location):
    import foundations

    data_from_file_stage = foundations.create_stage(_load_data_stage)
    features = data_from_file_stage(features_location)
    targets = data_from_file_stage(targets_location)

    return features, targets

def _model_package_for_retraining(preparation_stage, model_package_id):
    from foundations_production import load_model_package

    model_package = load_model_package(model_package_id)
    preprocessor = model_package.preprocessor
    preprocessor.set_inference_mode(False)

    return model_package

def _load_data_stage(file_location):
    from foundations_production.serving.data_from_file import data_from_file
    return data_from_file(file_location)

def create_job_workspace(job_id):
    import os
    from foundations_contrib.archiving import get_pipeline_archiver_for_job
    from foundations_contrib.job_source_bundle import JobSourceBundle

    workspace_path = '/tmp/foundations_workspaces/{}/'.format(job_id)
    os.makedirs(workspace_path, exist_ok=True)

    pipeline_archiver = get_pipeline_archiver_for_job(job_id)
    pipeline_archiver.fetch_job_source(workspace_path + '{}.tgz'.format(job_id))

    job_source_bundle = JobSourceBundle(job_id, workspace_path)
    job_source_bundle.unbundle(workspace_path)
    job_source_bundle.cleanup()

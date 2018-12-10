"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


def cleanup():
    import shutil
    from os import getcwd, remove
    from os.path import isdir
    from glob import glob
    from foundations.global_state import redis_connection
    from foundations.global_state import foundations_context
    from foundations_internal.pipeline_context import PipelineContext
    from foundations_internal.pipeline import Pipeline

    tmp_dir = getcwd() + '/tmp'
    if isdir(tmp_dir):
        shutil.rmtree(tmp_dir)

    for file in glob('*.tgz'):
        remove(file)

    redis_connection.flushall()

    pipeline_context = PipelineContext()
    pipeline = Pipeline(pipeline_context)
    foundations_context._pipeline = pipeline

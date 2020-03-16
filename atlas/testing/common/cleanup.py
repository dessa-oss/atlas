

def cleanup():
    import shutil
    from os import getcwd, remove
    from os.path import isdir
    from glob import glob
    from foundations_contrib.global_state import redis_connection, foundations_context
    from foundations_internal.pipeline_context import PipelineContext
    from foundations_internal.pipeline import Pipeline

    tmp_dir = getcwd() + '/foundations_home/job_data'
    if isdir(tmp_dir):
        shutil.rmtree(tmp_dir)

    for file in glob('*.tgz'):
        remove(file)

    pipeline_context = PipelineContext()
    pipeline = Pipeline(pipeline_context)
    foundations_context._pipeline = pipeline


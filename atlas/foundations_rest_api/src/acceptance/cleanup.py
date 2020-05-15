def cleanup():
    import shutil
    from os import getcwd, remove
    from os.path import isdir
    from glob import glob
    from foundations_rest_api.global_state import redis_connection
    import foundations_contrib.global_state
    from foundations_internal.foundations_job import FoundationsJob

    tmp_dir = getcwd() + '/tmp'
    if isdir(tmp_dir):
        shutil.rmtree(tmp_dir)

    for file in glob('*.tgz'):
        remove(file)

    redis_connection.flushall()

    foundations_contrib.global_state.foundations_job = FoundationsJob()

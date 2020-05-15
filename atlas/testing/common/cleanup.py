

def cleanup():
    import shutil
    from os import getcwd, remove
    from os.path import isdir
    from glob import glob
    import foundations_contrib.global_state
    from foundations_internal.foundations_job import FoundationsJob

    tmp_dir = getcwd() + '/foundations_home/job_data'
    if isdir(tmp_dir):
        shutil.rmtree(tmp_dir)

    for file in glob('*.tgz'):
        remove(file)

    foundations_contrib.global_state.foundations_job = FoundationsJob()
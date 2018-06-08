from stages import *
from vcat import *

def main():
    from uuid import uuid4

    config_manager.config()['deployment_implementation'] = {
        'deployment_type': LocalShellJobDeployment,
    }
    config_manager.config()['log_level'] = 'DEBUG'

    deployment_config = {
        'cache_implementation': {
            'cache_type': LocalFileSystemCacheBackend,
            'constructor_arguments': ['/tmp'],
        },
        'stage_log_archive_implementation': {
            'archive_type': LocalFileSystemPipelineArchive,
        },
        'persisted_data_archive_implementation': {
            'archive_type': LocalFileSystemPipelineArchive,
        },
        'provenance_archive_implementation': {
            'archive_type': LocalFileSystemPipelineArchive,
        },
        'job_source_archive_implementation': {
            'archive_type': LocalFileSystemPipelineArchive,
        },
        'artifact_archive_implementation': {
            'archive_type': LocalFileSystemPipelineArchive,
        },
        'miscellaneous_archive_implementation': {
            'archive_type': LocalFileSystemPipelineArchive,
        },
        'log_level': 'DEBUG',
    }

    pipe = pipeline | (load_data, '/home/thomas/Documents/test_data/Resources.csv') | describe

    job = Job(pipe)
    job_name = str(uuid4())

    bundle_name = str(uuid4())
    job_source_bundle = JobSourceBundle(bundle_name, '../')

    deployment = deployment_manager.deploy(deployment_config, job_name, job, job_source_bundle)
    wait_for_deployment_to_complete(deployment)

    result = deployment.fetch_job_results()
    log_manager.get_logger(__name__).debug('Got result: %s', repr(result))

if __name__ == "__main__":
    main()

from vcat import *
from vcat_ssh import *
from vcat_gcp import *

config_manager.config()['remote_user'] = 'thomas'
config_manager.config()['remote_host'] = 'localhost'
config_manager.config()['shell_command'] = '/bin/bash'
config_manager.config()[
    'code_path'] = '/home/thomas/Dev/Spiking/vcat-results/tmp/code'
config_manager.config()[
    'result_path'] = '/home/thomas/Dev/Spiking/vcat-results/tmp/results'
config_manager.config()['key_path'] = '/home/thomas/.ssh/id_local'
config_manager.config()['log_level'] = 'DEBUG'


# archive_listing = SSHListing()
archive_listing = LocalFileSystemPipelineListing('/home/thomas/Dev/Spiking/vcat-results/tmp/archives')

# with MultiSSHBundledPipelineArchive() as bundled_archive:
with LocalFileSystemPipelineArchive('/home/thomas/Dev/Spiking/vcat-results/tmp/archives') as bundled_archive:
    fetch = PipelineArchiverFetch(archive_listing, bundled_archive, bundled_archive,
                                  bundled_archive, bundled_archive, bundled_archive, bundled_archive)
    reader = ResultReader(fetch)
    print(reader.get_job_information())
    print(reader.get_results())
    reader.cleanup()

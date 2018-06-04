from vcat_ssh import SSHListing 
from vcat import config_manager

read_config = {
    'remote_user': 'thomas',
    'remote_host': 'localhost',
    'shell_command': '/bin/bash',
    'result_path': '/home/thomas/Dev/Spiking/vcat-results/tmp/results',
    'key_path': '/home/thomas/.ssh/id_local',
}
config_manager.config().update(read_config)

print(SSHListing().get_pipeline_names())


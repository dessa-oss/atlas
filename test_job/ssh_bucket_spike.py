from vcat import *
from vcat_ssh import *

config_manager.config()['log_level'] = 'DEBUG'
config_manager.config()['shell_command'] = '/bin/bash'
config_manager.config()['remote_user'] = 'thomas'
config_manager.config()['remote_host'] = 'localhost'
config_manager.config()['key_path'] = '/home/thomas/.ssh/id_local'

bucket = SSHFileSystemBucket('/home/thomas/Dev/Spiking/vcat-results/tmp/archives')

files = bucket.list_files('*.tracker')
print(files)
for path in files:
    print(bucket.download_as_string(path))
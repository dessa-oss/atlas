from vcat import *
from vcat_ssh import *

config_manager.config()['log_level'] = 'DEBUG'

bucket = SSHFileSystemBucket('/bin/bash', 'thomas', 'localhost', '/home/thomas/.ssh/id_local', '/home/thomas/Dev/Spiking/vcat-results/tmp/archives')

files = bucket.list_files('*.tracker')
print(files)
for path in files:
    print(bucket.download_as_string(path))
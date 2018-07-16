from foundations_gcp import *
from foundations import *

bucket = GCPBucket('tango-result-test')
bucket.upload_from_string('sandbox/hello', 'world')
with open('gcp_bucket_spike.py', 'rb') as file:
    bucket.upload_from_file('sandbox/gcp_bucket_spike.py', file)
print(bucket.download_as_string('sandbox/hello'))
with SimpleTempfile('w+b') as temp_file:
    bucket.download_to_file('sandbox/gcp_bucket_spike.py', temp_file.file)
    temp_file.flush()
    temp_file.seek(0)
    print(temp_file.read())
print(bucket.list_files('logs/*.log'))

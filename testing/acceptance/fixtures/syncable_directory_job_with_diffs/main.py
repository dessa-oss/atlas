"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import time
import foundations

first_directory = foundations.create_syncable_directory('some data', 'results')

time_of_upload = time.time()

with open(f'{first_directory}/time_of_upload.txt', 'w') as time_of_upload_file:
    time_of_upload_file.write(str(time_of_upload))

first_directory.upload()

time.sleep(10)

with open(f'{first_directory}/new_file.txt', 'w') as new_file:
    new_file.write('i am a new file, hello')

with open(f'{first_directory}/some_metadata.txt', 'w') as existing_metadata_file:
    existing_metadata_file.write('some modified metadata, why not')

first_directory.upload()
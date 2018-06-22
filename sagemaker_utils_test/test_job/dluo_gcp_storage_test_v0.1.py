'''
GCP Storage Test
Danny Luo

Reads data on bucket and writes it on data bucket again.

Users must be authenticated.

Followed my blog post on AWS S3 & boto3: https://dluo.me/s3databoto3
'''

import sys
import pandas as pd

from google.cloud import storage
from io import BytesIO

# Change bucket and file names here
bucket_name = 'tng-data-bucket'
file_name = 'iris.csv'
new_file_name = 'iris_2.csv' # new name to be re-uploaded as

# Setting up connection
client = storage.Client()
bucket = client.get_bucket(bucket_name)
blob = bucket.blob(file_name)

# Download as string (bytes), turn the read bytes as a file stream
df = pd.read_csv(BytesIO(blob.download_as_string()))

# Print off the first 5 lines of dataframe
print(df.head())

# Writing it back on GCP
new_blob = bucket.blob(new_file_name)
new_blob.upload_from_string(df.to_csv(index=False))

# Read it again to make sure there are no issues
df_new = pd.read_csv(BytesIO(new_blob.download_as_string()))
print(df_new.head())

import argparse
import uuid

from google.cloud.storage import Client
from googleapiclient import discovery

from vcat import *

def print_it(self):
  print(self)

pipe = pipeline | 'wonderful' | print_it

parser = argparse.ArgumentParser(description='Bundle a job.')
parser.add_argument('name', metavar='N', type=str, help='name of the job')
args = parser.parse_args()

def wait_for_job(job_name):
  import time

  gcp_bucket_connection = Client()
  result_bucket_connection = gcp_bucket_connection.get_bucket('tango-result-test')

  job_object = result_bucket_connection.blob(job_name + ".tgz")
  while not job_object.exists():
    print("waiting for job `" + job_name + "` to finish")
    time.sleep(6)
  
  print("job `" + job_name + "`completed, downloading results")
  with open(job_name + ".results.tgz", 'w+b') as file:
    job_object.download_to_file(file)

def get_results(job_name):
  import os
  import tarfile
  import pickle

  result = None
  with tarfile.open(job_name + ".results.tgz", "r:gz") as tar:
    for tarinfo in tar:
        if os.path.splitext(tarinfo.name)[1] == ".pkl":
            file = tar.extractfile(tarinfo)
            result = pickle.load(file)
            file.close()

  return result

job = Job(pipe)
job_name = str(uuid.uuid4())
save_job(job)
bundle_job(job_name)
GCPJobDeployment(job_name).deploy()
wait_for_job(job_name)
result = get_results(job_name)
print(result)
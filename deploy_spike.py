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

def wait_for_job(deployment):
  import time

  while not deployment.is_job_complete():
    print("waiting for job `" + deployment.job_name() + "` to finish")
    time.sleep(6)
  
  print("job `" + deployment.job_name() + "`completed")

job = Job(pipe)
job_name = str(uuid.uuid4())
save_job(job)
deployment = GCPJobDeployment(job_name)
deployment.deploy()
wait_for_job(deployment)
result = deployment.fetch_job_results()
print(result)
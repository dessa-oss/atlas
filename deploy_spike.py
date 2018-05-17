import argparse
from google.cloud.storage import Client
from googleapiclient import discovery

from vcat import *

def print_it(self):
  print(self)

pipe = pipeline | 'wonderful' | print_it

parser = argparse.ArgumentParser(description='Bundle a job.')
parser.add_argument('name', metavar='N', type=str, help='name of the job')
args = parser.parse_args()

class GCPJobDeployment(object):
  def __init__(self, job_name):
    self._job_name = job_name

  def deploy(self):
    gcp_bucket_connection = Client()
    result_bucket_connection = gcp_bucket_connection.get_bucket('tango-code-test')
    job_key = result_bucket_connection.blob(self._job_name + ".tgz")
    with open(self._job_name + ".tgz", 'rb') as file:
      job_key.upload_from_file(file)

save_pipeline(pipe)
bundle_pipeline(args.name)
GCPJobDeployment(args.name).deploy()


import argparse
import uuid

from vcat import *

def print_it(self):
  print(self)

pipe = pipeline | 'wonderful' | print_it

parser = argparse.ArgumentParser(description='Bundle a job.')
parser.add_argument('name', metavar='N', type=str, help='name of the job')
args = parser.parse_args()

job = Job(pipe)
job_name = str(uuid.uuid4())
save_job(job)
bundle_job(job_name)
GCPJobDeployment(job_name).deploy()


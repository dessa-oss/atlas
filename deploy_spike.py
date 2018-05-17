import argparse

from vcat import *

def print_it(self):
  print(self)

pipe = pipeline | 'wonderful' | print_it

parser = argparse.ArgumentParser(description='Bundle a job.')
parser.add_argument('name', metavar='N', type=str, help='name of the job')
args = parser.parse_args()  

save_pipeline(pipe)
bundle_pipeline(args.name)
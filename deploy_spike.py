from vcat import *

def print_it(self):
  print(self)

pipe = pipeline | 'wonderful' | print_it

def deploy(connector_wrapper, **kwargs):
  import tarfile
  
  job = Job(pipe)
  with open('job.bin', 'w+b') as file:
    file.write(job.serialize())

  tar = tarfile.open("job.tar", "w")
  for name in ["job.bin", "main.sh", "main.py", "requirements.txt", "vcat"]:
      tar.add(name)
  tar.close()
  
  return job

deploy(pipe)
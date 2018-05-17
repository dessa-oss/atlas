from vcat import *

def print_it(self):
  print(self)

pipe = pipeline | 'wonderful' | print_it

def deploy(connector_wrapper, **kwargs):
  import tarfile
  
  job = Job(pipe)
  with open('job.bin', 'w+b') as file:
    file.write(job.serialize())

  tar = tarfile.open("job.tgz", "w:gz")

  for name in ["job.bin", "run.sh", "main.py", "requirements.txt", "vcat"]:
      tar.add(name, arcname="job/" + name)
  tar.close()
  
  return job

deploy(pipe)
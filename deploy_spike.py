from vcat import *

def print_it(self):
  print(self)

pipe = pipeline | 'wonderful' | print_it

def deploy(job_name, connector_wrapper, **kwargs):
  import tarfile
  
  job = Job(pipe)
  with open("job.bin", "w+b") as file:
    file.write(job.serialize())

  with tarfile.open(job_name + ".tgz", "w:gz") as tar:
    for name in ["job.bin", "run.sh", "main.py", "requirements.txt", "vcat"]:
        tar.add(name, arcname=job_name + "/" + name)
  
  return job

deploy('wonderful1', pipe)
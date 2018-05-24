import uuid

from spike_pipe import print_it
from vcat import *

pipe = pipeline | 'wonderful' | print_it
pipe.persist()

def wait_for_job(deployment):
  import time

  while not deployment.is_job_complete():
    print("waiting for job `" + deployment.job_name() + "` to finish")
    time.sleep(6)
  
  print("job `" + deployment.job_name() + "`completed")

job = Job(pipe)
job_name = str(uuid.uuid4())
deployment = LocalShellJobDeployment(job_name, job)
deployment.deploy()
wait_for_job(deployment)
result = deployment.fetch_job_results()
print(result)

# pipe.run()
# pipeline_context = pipe._pipeline_context
# pipeline_context.save(GCPBundledResultSaver())

# job = Job(pipe)
# job_name = "test"
# bundler = JobBundler(job_name, {}, job)
# bundler.bundle()
# bundler.cleanup()
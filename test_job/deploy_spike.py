import uuid

from spike_pipe import print_it, destroy_it
from vcat import *

pipe = pipeline | 'wonderful' | print_it  # | destroy_it
pipe.persist()

job = Job(pipe)
job_name = str(uuid.uuid4())

bundle_name = str(uuid.uuid4())
job_source_bundle = JobSourceBundle(bundle_name, '../')
deployment = LocalShellJobDeployment(job_name, job, job_source_bundle)
# deployment = GCPJobDeployment(job_name, job, job_source_bundle)
# deployment.config()["result_savers"] = [
#     GCPResultSaver,
#     GCPBundledResultSaver
# ]
deployment.deploy()
wait_for_deployment_to_complete(deployment)
# raise_error_if_job_failed(deployment)
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

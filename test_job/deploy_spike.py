import uuid

from spike_pipe import print_it, destroy_it
from pandas import DataFrame
from vcat import *

# pipeline.cache = GCPCache()
pipe = pipeline | 'wonderful' | print_it  # | destroy_it
pipe2 = pipeline | 'wonderful' | print_it | destroy_it
pipe.persist()

job = Job(pipe)
job_name = str(uuid.uuid4())

bundle_name = str(uuid.uuid4())
job_source_bundle = JobSourceBundle(bundle_name, '../')
deployment = LocalShellJobDeployment(job_name, job, job_source_bundle)
# deployment = GCPJobDeployment(job_name, job, job_source_bundle)
deployment.config()['cache_implementation'] = {
    'cache_type': GCPCache,
    # 'constructor_arguments': [],
}
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

# pipeline_context.file_name = "test_job"
# # pipe.set_global_cache_name('wonderful.txt')
# # pipe.disable_caching()
# pipe.run()
# print(pipe.tree_names())
# print(pipe2.tree_names())
# # pipeline_context.provenance.job_source_bundle = JobSourceBundle('test_job', '../')
# # pipeline_context.provenance.job_source_bundle.bundle()
# # pipeline_listing = GCPPipelineArchiveListing()
# # with GCPPipelineArchive() as archive:
# # # with LocalPipelineArchive() as archive:
# #     archiver = PipelineArchiver(pipeline_context.file_name, pipeline_listing, archive, archive, archive, archive, archive, archive)
# #     pipeline_context.save_to_archive(archiver)

# #     pc = PipelineContext()
# #     pc.load_from_archive(archiver)

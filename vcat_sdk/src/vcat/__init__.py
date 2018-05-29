from vcat.gcp_bundle_fetcher import GCPBundleFetcher
from vcat.gcp_bundled_result_saver import GCPBundledResultSaver
from vcat.gcp_fetcher import GCPFetcher
from vcat.gcp_job_deployment import GCPJobDeployment
from vcat.gcp_result_saver import GCPResultSaver
from vcat.hyperparameter import Hyperparameter
from vcat.job import Job
from vcat.local_file_system_fetcher import LocalFileSystemFetcher
from vcat.local_file_system_result_saver import LocalFileSystemResultSaver
from vcat.local_shell_job_deployment import LocalShellJobDeployment
from vcat.pipeline_context import PipelineContext
from vcat.pipeline import Pipeline
from vcat.redis_fetcher import RedisFetcher
from vcat.redis_result_saver import RedisResultSaver
from vcat.result_reader import ResultReader
from vcat.stage_context import StageContext
from vcat.job_source_bundle import JobSourceBundle
from vcat.pipeline_archive_result_saver import PipelineArchiveResultSaver
from vcat.local_pipeline_archive import LocalPipelineArchive

def gcp_deploy_job(job, job_name):
  from uuid import uuid4

  bundle_name = str(uuid4())
  job_source_bundle = JobSourceBundle(bundle_name, '../')
  deployment = GCPJobDeployment(job_name, job, job_source_bundle)
  deployment.deploy()
  return deployment

def wait_for_deployment_to_complete(deployment):
  import time

  while not deployment.is_job_complete():
    print("waiting for job `" + deployment.job_name() + "` to finish")
    time.sleep(6)
  
  print("job `" + deployment.job_name() + "`completed")

def raise_error_if_job_failed(deployment):
  if deployment.is_job_complete():
    results = deployment.fetch_job_results()
    if results and results["error"]:
      raise results["error"]["type"], results["error"]["exception"], None

def restructure_headers(all_headers, first_headers):
  def diff(list_0, list_1):
    set_1 = set(list_1)
    return [item for item in list_0 if item not in set_1]

  return first_headers + diff(all_headers, first_headers)

pipeline_context = PipelineContext()
pipeline = Pipeline(pipeline_context)
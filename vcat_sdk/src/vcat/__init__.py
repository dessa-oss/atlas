from vcat.gcp_bundle_fetcher import GCPBundleFetcher
from vcat.gcp_bundled_result_saver import GCPBundledResultSaver
from vcat.gcp_fetcher import GCPFetcher
from vcat.gcp_job_deployment import GCPJobDeployment
from vcat.gcp_result_saver import GCPResultSaver
from vcat.hyperparameter import Hyperparameter
from vcat.job import Job
from vcat.job_source_bundle import JobSourceBundle
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
from vcat.pipeline_archiver import PipelineArchiver
from vcat.gcp_pipeline_archive import GCPPipelineArchive

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
  
  print("job `" + deployment.job_name() + "` completed")

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

def _grid_param_set_generator(hype_kwargs):
  import itertools

  hype_dict = {}

  for key, val in hype_kwargs.iteritems():
    if isinstance(val, list):
      hype_dict[key] = val
    else:
      hype_dict[key] = [val]

  param_keys = []
  param_vals_to_select = []

  for key, val in hype_dict.iteritems():
    param_keys.append(key)
    param_vals_to_select.append(val)

  for param_vals in itertools.product(*param_vals_to_select):
    param_set_entry = {}

    for param_key, param_val in zip(param_keys, param_vals):
      param_set_entry[param_key] = param_val

    yield param_set_entry

def grid_search(connector_wrapper, deployer_type, **hype_kwargs):
  import time
  import uuid

  for param_set in _grid_param_set_generator(hype_kwargs):
    connector_wrapper._reset_state()
    deployer_uuid = str(uuid.uuid4())

    bundle_base = deployer_uuid + "_bundle"

    job = Job(connector_wrapper, **param_set)
    job_source_bundle = JobSourceBundle(bundle_base, bundle_base)
    deployer = deployer_type(deployer_uuid, job, job_source_bundle)

    deployer.deploy()

    wait_for_deployment_to_complete(deployer)

    print deployer.fetch_job_results()

def _extract_results(results_dict):
  results = {}

  for result_entry in results_dict["results"].values():
    results.update(result_entry)

  return results

def adaptive_search(connector_wrapper, deployer_type, initial_generator, generator_function):
  import Queue
  import time
  import uuid

  queue = Queue.Queue()

  for initial_params in initial_generator:
    queue.put(initial_params)

  while not queue.empty():
    connector_wrapper._reset_state()

    param_set = queue.get()

    deployer_uuid = str(uuid.uuid4())
    bundle_base = deployer_uuid + "_bundle"

    job = Job(connector_wrapper, **param_set)
    job_source_bundle = JobSourceBundle(bundle_base, bundle_base)
    deployer = deployer_type(deployer_uuid, job, job_source_bundle)

    wait_for_deployment_to_complete(deployer)
    
    print deployer.fetch_job_results()

    for new_params in generator_function(_extract_results(results_dict)):
      queue.put(new_params)

pipeline_context = PipelineContext()
pipeline = Pipeline(pipeline_context)
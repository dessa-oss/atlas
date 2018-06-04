from preproc import *
from test_bullnet import *
from vcat import *
from vcat_gcp import *

import time

# training parameters
batch_size = 256
n_batches = 101

# hyperparameters
max_embedding = Hyperparameter("max_embedding")
emb_size_divisor = Hyperparameter("emb_size_divisor")
lr = Hyperparameter("lr")
l2 = Hyperparameter("l2")

bullnet_pipe = pipeline | preproc | (test_bullnet, batch_size, n_batches, max_embedding, emb_size_divisor, lr, l2)
bullnet_pipe.persist()

job = Job(bullnet_pipe, max_embedding=50, emb_size_divisor=2, lr=1e-4, l2=1e-3)
job_name = "job_bob_22"

job_source_bundle_name = "test_bundle"
job_source_bundle_path = "test_bundle"

job_source_bundle = JobSourceBundle(job_source_bundle_name, job_source_bundle_path)

deployment = LocalShellJobDeployment(job_name, job, job_source_bundle)

config = deployment.config()
config['cache_implementation'] = {
    'cache_type': GCPCacheBackend,
    # 'constructor_arguments': [],
}
config['archive_listing_implementation'] = {
    'archive_listing_type': GCPPipelineArchiveListing,
    # 'constructor_arguments': [],
}
config['stage_log_archive_implementation'] = {
    'archive_type': GCPPipelineArchive,
    # 'constructor_arguments': [],
}
config['persisted_data_archive_implementation'] = {
    'archive_type': GCPPipelineArchive,
    # 'constructor_arguments': [],
}
config['provenance_archive_implementation'] = {
    'archive_type': GCPPipelineArchive,
    # 'constructor_arguments': [],
}
config['job_source_archive_implementation'] = {
    'archive_type': GCPPipelineArchive,
    # 'constructor_arguments': [],
}
config['artifact_archive_implementation'] = {
    'archive_type': GCPPipelineArchive,
    # 'constructor_arguments': [],
}
config['miscellaneous_archive_implementation'] = {
    'archive_type': GCPPipelineArchive,
    # 'constructor_arguments': [],
}

deployment.deploy()
wait_for_deployment_to_complete(deployment)

print(deployment.fetch_job_results())

# bullnet_pipe.grid_search(LocalShellJobDeployment, max_embedding=[50], emb_size_divisor=2, lr=[1e-4], l2=1e-3)
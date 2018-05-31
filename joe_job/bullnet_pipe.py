from preproc import *
from test_bullnet import *
from vcat import *

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
job_name = "job_bob"

job_source_bundle_name = "test_bundle"
job_source_bundle_path = "test_bundle"

job_source_bundle = JobSourceBundle(job_source_bundle_name, job_source_bundle_path)

deployment = GCPJobDeployment(job_name, job, job_source_bundle)
deployment.deploy()
wait_for_deployment_to_complete(deployment)

print deployment.fetch_job_results()

# bullnet_pipe.grid_search(LocalShellJobDeployment, max_embedding=[50], emb_size_divisor=2, lr=[1e-4], l2=1e-3)
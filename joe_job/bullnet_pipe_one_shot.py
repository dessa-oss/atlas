from foundations import *
from staged_preproc import preproc
from staged_test_bullnet import test_bullnet

import time

# training parameters
batch_size = 256
n_batches = 101

# hyperparameters
max_embedding = Hyperparameter("max_embedding")
emb_size_divisor = Hyperparameter("emb_size_divisor")
lr = Hyperparameter("lr")
l2 = Hyperparameter("l2")

preproc_data = preproc()
bullnet_pipe = test_bullnet(preproc_data, batch_size, n_batches, max_embedding, emb_size_divisor, lr, l2)

params_dict = {
    'max_embedding': 50,
    'emb_size_divisor': 2,
    'lr': 1e-4,
    'l2': 1e-3
}

job = bullnet_pipe.run(params_dict)
print(job.fetch_job_results())
from vcat import *
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
    'max_embedding': IntegerHyperparameter(45, 56, 5),
    'emb_size_divisor': DiscreteHyperparameter([2]),
    'lr': FloatingHyperparameter(min=1e-5, max=1.1e-4, step=1e-4),
    'l2': DiscreteHyperparameter([1e-3])
}

deployments_map = bullnet_pipe.grid_search(params_dict)

wait_on_deployments_map(deployments_map)
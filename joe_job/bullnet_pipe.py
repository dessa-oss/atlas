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
    'max_embedding': IntegerHyperparameter(45, 51, 5),
    'emb_size_divisor': DiscreteHyperparameter([2]),
    'lr': FloatingHyperparameter(min=2e-5, max=1.2e-4, step=1e-4),
    'l2': DiscreteHyperparameter([1e-3])
}

deployment_set = bullnet_pipe.random_search(params_dict, max_iterations=5)
wait_on_deployment_set(deployment_set)

# def create_params():
#     return {
#         'max_embedding': IntegerHyperparameter(45, 51, 5).random_sample(),
#         'emb_size_divisor': DiscreteHyperparameter([2]).random_sample(),
#         'lr': FloatingHyperparameter(min=2e-5, max=1.2e-4, step=1e-4).random_sample(),
#         'l2': DiscreteHyperparameter([1e-3]).random_sample()
#     }

# state = 2

# def params_generation(result):
#     global state

#     print("within params: " + str(result))
#     print("state: " + str(state))

#     for _ in range(state):
#         yield create_params()
    
#     state -= 1

# bullnet_pipe.adaptive_search([create_params()], params_generation)
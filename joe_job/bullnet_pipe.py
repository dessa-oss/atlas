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
    'lr': DiscreteHyperparameter([1e-4, 1e-5]),
    'l2': DiscreteHyperparameter([1e-3])
}

deployments_map = bullnet_pipe.grid_search(params_dict)

time_to_sleep = 5

while deployments_map != {}:
    jobs_done = []

    for job_name, deployment in deployments_map.items():
        job_status = deployment.get_job_status()

        print(job_name + ": " + job_status)

        if deployment.is_job_complete():
            print deployment.fetch_job_results()
            jobs_done.append(job_name)

    for job_name in jobs_done:
        deployments_map.pop(job_name)

    print("----------\n")

    time.sleep(time_to_sleep)
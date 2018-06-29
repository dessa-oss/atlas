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

deployment = bullnet_pipe.run(max_embedding=50, emb_size_divisor=2, lr=1e-4, l2=1e-3)

time_to_sleep = 1

while not deployment.is_job_complete():
    result = deployment.get_job_status()
    
    if result == "Running":
        time_to_sleep = 5

    print(result)
    time.sleep(time_to_sleep)

print(deployment.get_job_status())
print(deployment.fetch_job_results())
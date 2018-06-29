from preproc import *
from test_bullnet import *
from vcat import *

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
print(deployment.fetch_job_results())

# Returns "Completed" finished successfully, "Error" if finished but unsuccessful
print(deployment.get_job_status())
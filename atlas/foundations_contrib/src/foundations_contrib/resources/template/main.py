"""
This sample main.py shows basic Atlas functionality.
In this script, we will log some arbitrary values & artifacts that can be viewed in the Atlas GUI
"""

import foundations

depth = 3
epochs = 5
batch_size = 256
lrate = 1e-3


# Log some hyper-parameters
foundations.log_param('depth', depth)
foundations.log_params({'epochs': epochs,
                        'batch_size': batch_size,
                        'learning_rate': lrate})

# Log some metrics
accuracy = 0.9
loss = 0.1
foundations.log_metric('accuracy', accuracy)
foundations.log_metric('loss', loss)

# Log an artifact that is already saved to disk
foundations.save_artifact('README.txt', 'Project_README')
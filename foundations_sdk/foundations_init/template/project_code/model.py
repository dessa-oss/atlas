"""
Each function here can be considered as a step (stage) towards building a model.

Although we don't use foundations in this simple example, we import Foundations as it quickly becomes useful once want to use features like `.log_mteric()` within stage functions.

We create a simple function that adds 10 to a number that will be used as a stage in our driver file.
"""

import foundations

def dummy_function(x):
	return x + 10
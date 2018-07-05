"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


import vcat
import vcat_mlflow
import mlflow

from staged_methods import *
from random import randint

# create a stage from the create_data_frame method
data = create_data_frame()

# union the data frame with itself
data = scale_data(data, vcat.Hyperparameter("scale"))

# execute the stage locally with mlflow
with mlflow.start_run():
    data.run_same_process(scale=randint(5, 15))

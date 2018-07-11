"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""


import vcat
import vcat_ui

from staged_methods import create_data_frame, scale_data
from random import randint

# create a stage from the create_data_frame method
data = create_data_frame()
data.persist()

# union the data frame with itself
data = scale_data(data, vcat.Hyperparameter("scale"))
data.persist()

# execute the stage locally with vcat_ui
with vcat_ui.start_run():
    data.run_same_process(scale=randint(5, 15))

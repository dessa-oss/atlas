"""
This file is used for your model code, and for organizing and executing Foundations stages.

Below we import foundations, as well as a function from our model file that we'll use as a stage.

We then tell Foundations how to run by defining a path to a configuration file.

Next we define a project name using `set_project_name`.

We define the experiment to run as `result` and the `.run()` which tells Foundations to run these stages.
"""

import foundations
from model import dummy_function

foundations.config_manager.add_config_path('../config/default.local.yaml')
foundations.set_project_name('my-foundations-project')

dummy_function = foundations.create_stage(dummy_function)

# input to model
x = 20

# build step1 of model
result = dummy_function(x)

# run the model
result.run()
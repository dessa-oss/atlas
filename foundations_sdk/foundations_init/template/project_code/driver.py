"""
This file is used for your model code, and for organizing and executing Foundations stages.

Below we import foundations, and then tell it how to run by giving foundations a path to a configuration file.

We then use `set_project_name` to give the project a name.


...expand

"""

import foundations
from model import dummy_function

dummy_function1 = foundations.create_stage(dummy_function1)

foundations.config_manager.add_config_path('../config/default.local.yaml')
foundations.set_project_name('my-foundations-project')

# input to model
x = 20

# build step1 of model
result = dummy_function1(x)

# run the model
result.run()
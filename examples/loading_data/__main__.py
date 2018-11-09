"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

"""
This very simple module shows the lightweight syntax introduced by Foundations.
After importing Foundations, you can import the modules containing code you created
as usual. You can then create stages with any imported function using create_stage().

With create_stage(), Foundations does some magic that wraps your code in layers
which perform provenance tracking, caching, prepping your job for deployment to compute, and so on.

The "main" code below is exactly what you'd write without Foundations, save for that
.run() method.  That method deploys your job to some configured compute - could be GCP,
your local machine, or even an NVIDIA DGX! (Check out the example_configs folder to learn how how to 
modify your configuration to deploy remotely.) You can in principle use the .run() method
on any stage, but using it on the final stage is usually what you want.
"""

import foundations
from common.data import load_titanic
from common.logging import log_data, log_formatted

# set configuration for running the job 
foundations.config_manager.add_config_path('config/local_default.config.yaml')

load_titanic = foundations.create_stage(load_titanic)
log_data = foundations.create_stage(log_data)

"""
Once the stage is created, if we want to debug and understand which stage is 
running we can use StageConnectorWrapper's .name() to see the stage name
"""
stage = log_data(load_titanic())
log_formatted(stage.name())

if __name__ == '__main__':
    data = load_titanic()
    log_data(data).run()

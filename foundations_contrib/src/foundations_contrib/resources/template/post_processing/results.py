"""

This goal of this file interact with results once experiments have run.

After importing Foundations we set the configuration to be used using `foundations.config_manager.add_config_path()`.

Then to get all experiment results from a particular project we use `foundations.get_metrics_for_all_jobs()`.

"""

import foundations

foundations.get_metrics_for_all_jobs("my-foundations-project")
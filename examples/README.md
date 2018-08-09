# Foundations Examples

The purpose of this directory is to provide examples of Foundations-based code in action as well as explanations of what specific pieces of the Foundations API allow you to do.

To run any of these examples, first `pip install -r requirements.txt` and then `python -m <main_module_name>`.  Make sure to install Foundations as well, of course.  Let's now go through the main modules that exist here (in alpha order) as well what they aim to show.  We'll also quickly talk the library modules in this directory - they aren't intended to be run.

Each python file in each subdirectory contains a more in-depth description of what the code is doing, should you want further information.

## Main Modules

### cache

This module demonstrates the use of a user-configured global cache, which allows multiple jobs to share the same output data from stages they all use.  If two jobs, A and B, are essentially the same until halfway (say), the first half of B should not need to be executed if A has already run.  B can use A's data if global caching is enabled.

`python -m cache`

### fetch_job_information

This module demonstrates the use of the result reader.  Specifically, it demonstrates using the result reader to grab job metadata for jobs that have already run.  Job metadata includes how long a job took to run as well as job name and how stages connect to each other.  There's no point in running this module if you haven't run a job - run the hyperparameter_search module or logistic_regression module first to generate some illustrative output.

`python -m fetch_job_information`

### fetch_results

This module demonstrates the use of the result reader.  Specifically, it demonstrates using the result reader to grab job results for jobs that have already run.  A job result is something explicitly logged by the user in their stage function code.  There's no point in running this module if you haven't run a job - run the hyperparameter_search module or logistic_regression module first to generate some illustrative output.

`python -m fetch_results`

### hyperparameter_search

This module gives an example implementation of hyperparameter search using the Hyperparameter placeholder provided by Foundations as well as calling the `.run()` method with multiple parameters.  See `hyperparameter_search/__main__.py` for more in-depth information.

`python -m hyperparameter_search`

### impute_data

Simple illustration of the unobtrusiveness of Foundations syntax.

`python -m impute_data`

### loading_data

Simple illustration of the unobtrusiveness of Foundations syntax.

`python -m loading_data`

### local_cache

This module demonstrates how Foundations handles redundant execution.  If you have one stage whose result feeds into more than one downstream stage, the result should not be recomputed.  Since the result is in memory already, the downstream stages should simply read from memory the result of the upstream stage.  Foundations implements this internally, and is always enabled.

`python -m local_cache`

### logistic_regression

Titanic!  The code in this module applies a logistic regression model to the Titanic dataset.  This module mainly serves to demonstrate the use of the `.splice()` method.  If you have a stage that returns multiple items e.g. in a list, you may want to use the splat syntax: `x, y = return_two_things()`.  Unfortunately, due to Python's type system (among other things), there's no way for Foundations to know how many elements a stage may want to pass down to downstream stages.  The user has to provide a tiny bit of help via the `.splice()` method.  See `logistic_regression/__main__.py` for examples.

`python -m logistic_regression`

### one_hot_encode

Simple illustration of the unobtrusiveness of Foundations syntax.

`python -m one_hot_encode`

### replacing_nulls

Simple illustration of the unobtrusiveness of Foundations syntax.

`python -m replacing_nulls`

## Library Modules

### common

Contains code used across the above modules.  Mostly ETL code and such in this directory.

### config

Loads config used by Foundations to determine where to store job results as well as where to deploy a job.

### titanic

Contains ETL code specific to the titanic example.
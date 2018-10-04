# Foundations Examples

The purpose of this directory is to provide examples of Foundations-based code in action as well as explanations of what specific pieces of the Foundations API allow you to do.

To run any of these examples, first `pip install -r requirements.txt` and then `python -m <main_module_name>`.  Make sure to install Foundations as well, of course.  Let's now go through the main modules that exist here (in alpha order) as well what they aim to show.  We'll also quickly talk the library modules in this directory - they aren't intended to be run.

Each python file in each subdirectory contains a more in-depth description of what the code is doing, should you want further information.

If you'd like a place to start, have a look at [impute_data](./impute_data/__main__.py).

For an example of how to structure model code for Foundations, have a look at [common/models.py](./common/models.py).

## Main Modules

### [cache](./cache/__main__.py)

This module demonstrates the use of a user-configured cache, which allows multiple jobs to share the same output data from stages they all use.  If two jobs, A and B, are essentially the same until halfway (say), the first half of B should not need to be executed if A has already run.  B can use A's data if this form of caching is enabled (there is another form of caching, which will be demonstrated in another module).

`python -m cache`

### [fetch_job_information](./fetch_job_information/__main__.py)

This module provides an example of how to grab information for a completed job.  Specifically, it demonstrates using a class Foundations provides in order to grab job metadata for jobs that have already run.  Job metadata includes how long a job took to run as well as job name and how stages connect to each other.  There's no point in running this module if you haven't run a job - run the grid_search module or logistic_regression module first to generate some illustrative output.

`python -m logistic_regression && python -m fetch_job_information`

### [fetch_job_metrics](./fetch_job_metrics/__main__.py)

This module provides an example of how to grab information for all completed jobs in a named project with the `get_metrics_for_all_jobs` method. Job metadata includes job input parameters, job output results, and additional data including how long a job took to run. There's no point in running this module if you haven't run a job with a project name - run the grid_search module or logistic_regression module first to generate some illustrative output.

`python -m logistic_regression && python -m fetch_job_metrics`

### [fetch_results](./fetch_results/__main__.py)

This module provides an example of how to grab results for a completed job.  Specifically, it demonstrates using a class Foundations provides in order to grab job results for jobs that have already run.  A job result is something explicitly logged by the user in their stage function code.  There's no point in running this module if you haven't run a job - run the grid_search module or logistic_regression module first to generate some illustrative output.

`python -m logistic_regression && python -m fetch_results`

### [grid_search](./grid_search/__main__.py)

This module gives an example implementation of hyperparameter (grid) search using the Hyperparameter placeholder provided by Foundations as well as calling the `.grid_search()` method with ranges of parameters.  See the source file for more in-depth information.

`python -m grid_search`

### [impute_data](./impute_data/__main__.py)

Simple code example showing how easy it is to structure code in a Foundations-compatible way.  This particular example demonstrates data imputation - filling null or empty entries in a dataset with a dynamically-computed value (usually the mean of non-empty values).

`python -m impute_data`

### [loading_data](./loading_data/__main__.py)

Simple code example showing how easy it is to structure code in a Foundations-compatible way.  This particular example demonstrates loading data from a csv.

`python -m loading_data`

### [local_cache](./local_cache/__main__.py)

This module demonstrates how Foundations handles redundant execution.  If you have one stage whose result feeds into more than one downstream stage, the result should not be recomputed.  Since the result is in memory already, the downstream stages should simply read from memory the result of the upstream stage.  Foundations implements this particular form of caching internally, and is always enabled.

`python -m local_cache`

### [logistic_regression](./logistic_regression/__main__.py)

Titanic!  The code in this module applies a logistic regression model to the Titanic dataset - see [this link](https://www.kaggle.com/c/titanic) for more info.  This module mainly serves to demonstrate the use of the `.split()` method, provided as part of the Foundations API.  If you have a stage that returns multiple items e.g. in a list, you may want to use the splat syntax: `x, y = return_two_things()`.  Unfortunately, due to Python's type system (among other things), there's no way for Foundations to know how many elements a stage may want to pass down to downstream stages.  The user has to provide a tiny bit of help via the `.split()` method. The module also shows you how to name jobs in your project through the `.set_project_name('project_name')` method. 

`python -m logistic_regression`

### [one_hot_encode](./one_hot_encode/__main__.py)

Simple code example showing how easy it is to structure code in a Foundations-compatible way.  This particular example demonstrates one-hot encoding - taking a column of data whose type is categorical / an enumeration and encoding it using [one-hot vectors](https://en.wikipedia.org/wiki/One-hot).

`python -m one_hot_encode`

### [replacing_nulls](./replacing_nulls/__main__.py)

Simple code example showing how easy it is to structure code in a Foundations-compatible way.  This particular example demonstrates replacing null or empty values in a dataset with a constant, user-specified value.

`python -m replacing_nulls`

## Library Modules

### [common](./common)

Contains code used across the above modules.  Specifically, csv reading, logging, convenience classes, reusable ETL code, and the model itself.  This code has nothing to do with Foundations itself and exists only to support the main example modules.

### [config](./config/__init__.py)

Loads config used by Foundations to determine where to store job results as well as where to deploy a job.

### [titanic](./titanic/etl.py)

Contains ETL code specific to our solution of the [Titanic problem](https://www.kaggle.com/c/titanic).

## Configuration Examples

Foundations uses a configuration-driven approach to deployment. [Config Examples](./example_configs) gives examples on how to setup config for different enviornments.
 

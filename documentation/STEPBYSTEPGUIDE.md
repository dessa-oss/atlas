# Step by step Guide

## Step 1: Writing a model code

Consider a naive model which takes an input(x), increases it's value by 10 and then multiples it(x+10) by some value(y) to output result(y * (x+10))

This very naive model code is all under one package.
The example package is [here](sample_code).
This package has a [naive model](sample_code/model.py).

This model consists of two steps:
1. To increase value by 10
2. To multiply this increased value by a given number

In the end, this model outputs a multiplied value.

For best coding practices we recommend breaking down model code into different small functions(steps). Structuring code into functions makes for more maintainable and re-usable code in the long run.

**Note: Entire model code is written in model.py. The foundations deploy specific code is written in deploy.py. Code in deploy.py is just using all functions defined in model.py**

## Step 2: Use Foundations to run model code

The [driver.py file](sample_code/driver.py) shows how to use Foundations to run model code. Let's look at it line by line.

```
import foundations
from models.model import incr_by_10, mult
incr_by_10 = foundations.create_stage(incr_by_10)
mult = foundations.create_stage(mult)
```
`incr_by_10` function is wrapped through Foundations.
Similary,  `mult` function is wrapped through Foundations.

```
# build step1 of model
incr_value = incr_by_10(x)
```
This step doesn't execute `incr_by_10` function, it creates a pointer to the first step of the model. When this function is executed the return value from the function is wrapped in an object which is assigned to `incr_value` variable, from here on we call it `stage_object`.

```
# build step2 of model
result = mult(x, incr_value)
```
This behaves the same as above, `result` is `stage_object`. Notice, we are passing `incr_value` to `mult` function. `incr_value` is a stage_object and has not been executed yet.

```
# run the model
result.run()
```
To execute any stage, we need to invoke `run` function on the stage_object. This step will execute the stage and any dependent stage it needs to invoke.

To run this job, you need to run `python driver.py` from terminal. It should run the model code through Foundations and track of lot of metadata about the run.

## Step 3: Add project name for your experiments

You will probably be running multiple jobs to train a model. We recommend to define a project and store all information about your jobs and results under one this project name space. You can do this by setting project_name in your code.
For example, in `driver.py` file, add
```
foundations.set_project_name("demo_project")
```
Everytime, a new job is ran, all results and job information coming out of this job will be stored under project space 'demo_project'.


## Step 4: Log metrics in your model stages

We suspect, you want to log metrics (so that you can evaluate them later) in your job runs when you are training your model. You can do this by using log_metric function.
For example, in `model.py` file:
```
foundations.log_metric('x', x)
```
This will log value of x with key as `x` in Foundations backend.

```
foundations.log_metric('y', y)
```
This will log value of y with key as `y` in Foundations backend.
These values of x and y will be available to read after jobs finish running.

## Step 5: Reading logged metrics

Now that you have logged some metrics during model training, you want to read them after all your jobs are finished so that you can analyse your metrics. You can get all these metrics using get_metrics_for_all_jobs(project_name) on foundations:
```
Start a python interpreter and run following commands:
import foundations
foundations.get_metrics_for_all_jobs("demo_project")
```
This will read logged metrics for jobs ran under project name `demo_project`. It returns a pandas data frame.

## Step 6: Use Foundations caching feature

Now, that you know how to log and read metrics for each job, you want to train best model possible. You will be running jobs (model code) with various different data inputs and parameters. In these numerous jobs many computations will be similar, so Foundations has a smart way of detecting these identical computations across all jobs and re-using the already computated step instead of re-computing everytime for every job. We call it caching.
You will have to tell Foundations which step might get recomputed. This can be done by using enable_caching() on `stage_object`.
For example, in `driver.py` file:
```
incr_value.enable_caching()
```
This will enable the caching feature on `incr_value` stage_object. For every job ran, the return value from `incr_value` will be cached in Foundations. 
Therefore, if first job runs `incr_value(3)` then its return value of `13` will be cached in Foundations. When second job runs `incr_value(3)`, Foundations will directly use pre-computed cached value `13` instead of re-computing this step. You can imagine how powerful this feature can become in model training.


## Step 7: Use Foundations ResultReader to inspect your job

Now that you've run your job, you may want to retrieve specific metrics about the individual stages within your job including how long they took to run, the input parameters, the output results, and maybe even the source code. The ResultReader class provides a way to do this with a set of methods.

First create an instance of ResultReader
```
import foundations
from foundations import ResultReader, JobPersister

with JobPersister.load_archiver_fetch() as fetch:
    reader = ResultReader(fetch)
```
With your ResultReader, you can now use the following methods. 

```
reader.get_results()
```

   Similar to `foundations.get_metrics_for_all_jobs()`, `get_results()` will get the results for all jobs run, irrespective of their project name.   

```
reader.get_job_information()
```

This gets the stage level information for all stages run, for all jobs. 

```
reader.get_source_code(stage_id)
```

This fetches the source code of a given stage. 

```
reader.get_unstructured_results(job_id, stage_id)
```

If a stage has outputs that have been persisted with `.persist()`, this function will return the list of these outputs. 

```
reader.get_error_information(job_id, <option stage_id>)
```

Returns the stack trace for either the job or the specific stage specified, if it fails. If there is no failure, this will return None.

```
reader.create_working_copy(pipeline_name, path_to_save)
```

Creates a copy of your job sourc
e in a different location. 

## Step 8: Adding additional dependencies (optional)

Be aware that installing a package locally doesn't mean it will be in the execution environment. If you want to use an external python package, you'll need to create a `requirements.txt` wherever your model code exists with the dependencies explicitly stated. The requirements file will be in the root of the model code directory. For an example of this, see where the [requirements.txt in /examples](https://github.com/DeepLearnI/foundations/tree/master/examples) sits.

Reference the main [STARTGUIDE](https://github.com/DeepLearnI/foundations/blob/master/documentation/STARTGUIDE.md) for a more detailed explanation.
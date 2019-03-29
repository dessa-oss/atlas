<h1>Getting Started with Foundations</h1>

In this tutorial we will go over how to build and deploy a model using Foundations, as well as demonstrate additional features. To use Foundations to its maximum extent, we recommend seperating any job deployment code from the actual model itself. For this example, we will seperate all model code into a file called model.py and any job deployment code into deploy.py which will just use the functions defined in model.py.

This tutorial will also be using Jupyter Notebook as the primary interface to deploy model code locally; however, Foundations is **not** dependant of Jupyter Notebook and models can be deployed natively through Python. For those wishing to run the code without Jupyter, simply run the driver code with the Foundations CLI command: `foundations deploy project_code/driver.py --env=local`.

<h3>Before you start</h3>

You should have already [installed Foundations](../quick_start/) as well as [Jupyter Notebook](../start_guide/#jupyter-notebook-setup) up and runnning.

## Step 0: Set your configuration (optional)

If you are:

 - Planning on running your foundations code on a remote environment like Google Cloud Platform (GCP) or SSH
 - Want to modify where foundations stores data when running locally
 - Want to setup a cache
 - Looking to modify the verbosity of foundations logs
 - Looking to set environment variables in your deployment environment

 you can customize your configurations. Instructions and examples on how to do this can be found [here](../configs/).


 *By default, foundations will deploy locally, running your code on your local machine.*

## Step 1: Writing model code

In Jupyter, navigate to the project directory. In `project_code` you should find a `model.py` and `driver.py` file. Open the `model.py` file and follow the instructions below:

Replace the contents of the `model.py` file the following code:
```python
# Naive model code
# Each function here can be consider as a step (stage) towards building a model.
import foundations

def incr_by_10(x):
	return x + 10

def mult(x, y):
	output = x * y
	foundations.log_metric('output', output)	
	return output
```

Here we have a basic model which takes an input(x), increases it's value by 10 and then multiples it by some value (y) to output result (y * (x+10))

This model consists of two steps:  
1. To increase value by 10  
2. To multiply this increased value by a given number

In the end, this model outputs a multiplied value.

For best coding practices we recommend breaking down model code into different small functions(steps). Structuring code into functions makes for more maintainable and re-usable code in the long run.

## Step 2: Use Foundations to run model code

Create a new notebook called `driver.ipynb` in the project root directory and add the code below. The following file shows how to shows how to use Foundations to run model code.
```python
import foundations
from project_code.model import incr_by_10, mult

incr_by_10 = foundations.create_stage(incr_by_10)
mult = foundations.create_stage(mult)

# input to model
x = 20

# build step1 of model
incr_value = incr_by_10(x)

# build step2 of model
result = mult(x, incr_value)

# run the model
result.run()
```
Let's break it down line by line:

```python
import foundations
from project_code.model import incr_by_10, mult

incr_by_10 = foundations.create_stage(incr_by_10)
mult = foundations.create_stage(mult)
```
The function `incr_by_10` function is wrapped through Foundations, converting into a `stage_object` which Foundations uses to understand the pieces of building a model. Similary, `mult` function is wrapped through Foundations.

```
# build step1 of model
incr_value = incr_by_10(x)
```
This step doesn't execute `incr_by_10` function since it's wrapped as a stage by Foundations, rather it creates a pointer to the first step of the model. When this function is executed the return value from the function is wrapped in an object which is assigned to `incr_value` variable instead. From here on we call it a `stage_object` which will be handled by Foundations later on.

```
# build step2 of model
result = mult(x, incr_value)
```
This behaves the same as above where `result` is now a `stage_object` since it's been wrapper by Foundations as a stage. Notice, we are passing `incr_value` to the function. `incr_value` is a stage_object and has not been executed yet.

```
# run the model
result.run()
```
To execute any stage, we need to invoke `run` function on the stage_object. This step will execute the stage and any dependent stage it needs to invoke. 

Finally, before deploying the job, we need to specify the deployment environment in the notebook. Before the `.run()` function, we need to run the following line in Jupyter to specify to Foundations what environment to run the job in:

```python
foundations.set_environment('local')
```
This line specifies the location of the configuration file which Foundations will reference for deployment details of the job. For this tutorial, we will only deploy job in our local environment; however, Foundations supports deploying to remote environments as well which can be specified with different configuration files. More information can be found [here](../configs/).

To deploy the job, run the cell containing the `.run()` function. Give it a try!

## Step 3: Specifying project names for your experiments

You've just run your first job! You should be able to view the job in the [Web GUI](../gui/) at `https://localhost:6443` under `default`.

You will probably be running multiple jobs to train a model. We recommend defining a project and storing all information about your jobs and results under one this project name space. You can do this by setting project names in your code.
For example, in `driver.py` file, add
```
foundations.set_project_name("demo_project")
```

before `.run()`. Everytime, a new job is ran, all results and job information coming out of this job will be stored under project space 'demo_project'. Rerunning the job should now have a new project on the GUI under "demo_project"

## Step 4: Log metrics in your model stages

To log metrics (so that you can evaluate them later) in your job runs when you are training your model, you can use the `log_metric` function.
For example, in `model.py` file lets add the following lines in `mult(x, y)`:
```python
foundations.log_metric('x', x)
foundations.log_metric('y', y)
```

This will log value of x with key as `x` and y with key as `y` in Foundations backend.
These values of x and y will be available to read after jobs finish running.

## Step 5: Reading logged metrics

Now that you have logged some metrics during model training, you want to read them after all your jobs are finished so that you can analyse your metrics. You can get all these metrics using get_metrics_for_all_jobs(project_name) on foundations:
```
Start a python interpreter and run following commands:
import foundations
foundations.get_metrics_for_all_jobs("demo_project")
```
To run this is in Jupyter, you can create a new cell and directly run the line above. This will read logged metrics for jobs ran under project name `demo_project`. It returns a pandas data frame.

## Step 6: Use Foundations caching feature

Now, that you know how to log and read metrics for each job, you want to train best model possible. You will be running jobs (model code) with various different data inputs and parameters. In these numerous jobs many computations will be similar, so Foundations has a smart way of detecting these identical computations across all jobs and re-using the already computated step instead of re-computing everytime for every job. We call it caching.
You will have to tell Foundations which step might get recomputed. This can be done by using enable_caching() on `stage_object`.
For example, in `driver.py` file let's add:
```
# build step1 of model
incr_value = incr_by_10(x)
incr_value.enable_caching()
```
This will enable the caching feature on `incr_value` stage_object. For every job ran, the return value from `incr_value` will be cached in Foundations.
Therefore, if first job runs `incr_value(3)` then its return value of `13` will be cached in Foundations. When second job runs `incr_value(3)`, Foundations will directly use pre-computed cached value `13` instead of re-computing this step. You can imagine how powerful this feature can become in model training.

## Step 7: Deploying to Remote Environments (optional)

To run jobs on remote environments, you will need to use different configuration files and additional resources when deploying the job. This can be done via configuration file management 

In addition, you may need to set environment variables in your notebook first before deploying the job. For example, to deploy on GCP, you will need a environment variable pointing to a JSON keyfile:

```bash
%env GOOGLE_APPLICATION_CREDENTIALS=/absolute/path/to/keyfile.json
```

For more information on deploying to remote environments, please refer to the documentation [here](../configs/)

## Step 8: Adding additional dependencies (optional)

Be aware that installing a package locally doesn't mean it will be in the execution environment. If you want to use an external python package, you'll need to create a `requirements.txt` wherever your model code exists with the dependencies explicitly stated. The requirements file will be in the root of the model code directory. 

Reference the main [start guide](../start_guide/) for a more detailed explanation.

## Complete Tutorial Code
```python
# driver.py
import foundations
from project_code.model import incr_by_10, mult

incr_by_10 = foundations.create_stage(incr_by_10)
mult = foundations.create_stage(mult)

foundations.set_project_name("demo_project")

# input to model
x = 20

# build step1 of model
incr_value = incr_by_10(x)
incr_value.enable_caching()

# build step2 of model
result = mult(x, incr_value)

# run the model
result.run()
```
```python
# model.py
# Naive model code
# Each function here can be consider as a step (stage) towards building a model.
import foundations

def incr_by_10(x):
    return x + 10

def mult(x, y):
    foundations.log_metric('x', x)
    foundations.log_metric('y', y)
    output = x * y
    foundations.log_metric('output', output)    
    return output
```

<h1>Scheduling Mode</h1>
---

This mode enables advanced usage of Atlas. It is well suited for running large hyperparameter searches across multiple projects. 
Scheduling mode also allows complete use of the CLI commands used to interact with jobs. 
In Scheduling mode, experiments are submitted to the local Atlas Scheduler and are queued for execution inside a Worker. 
The contents of the users current working directory are moved to an Atlas working directory and mounted inside the Worker. 
The results are then stored in an archive location that can be accessed using the CLI.    

!!! note
    Atlas comes with a Docker based local scheduler out of the box. The installation also sets up a configuration file called `scheduler.config.yaml`, this is the `scheduler_config`
    that is used for most CLI and SDK commands.
    
    See [here](https://dessa-atlas-community-docs.readthedocs-hosted.com/en/latest/atlas-modes/scheduling/#submitting-to-a-remote-scheduler) to see how you can create a new scheduler config to launch to a remote machine.  

### Creating a project
Use the `foundations init <project_name>` command to create a template project directory. This command will create a project directory in your current directory with the following contents:

```python
foundations init my_project
```
```
my_project
|--- README.txt
|--- data
|--- job.config.yaml
|--- main.py
```

The template provides a sample `main.py` which logs a few arbitrary metrics & saves an artifact to demonstrate in the GUI. 
We can use this `main.py` to submit our first job to the scheduler.

Also included in the project directory is an empty data folder, a README and a sample job configuration `job.config.yaml`.
We will explore the job configuration in more detail in a later section.   

### Submitting a single job to the Scheduler
The `foundations submit` CLI command is used to submit jobs to a scheduler. 
We can submit our `main.py` to the scheduler for execution as follows:

```python
foundations submit scheduler . main.py
``` 

Once this command is executed, we'll start seeing logs streaming in the console:
```
Foundations INFO: Job submission started. Ctrl-C to cancel.
Foundations INFO: Preparing to bundle contents of /home/<user>/code/my_project for execution. Estimating bundle size.
Foundations INFO: Bundling job contents.
Foundations INFO: Job submitted with ID '45540b52-ffe2-44ab-9838-db467d3499c0'.
Foundations INFO: Job queued. Ctrl-C to stop streaming - job will not be interrupted or cancelled.
Foundations INFO: Job running, streaming logs.
========================================================================================================================
No user requirements found.
========================================================================================================================
Foundations INFO: Job '45540b52-ffe2-44ab-9838-db467d3499c0' has completed.
```

We can also view the job status and any captured metadata in the GUI as usual.

This CLI command takes three positional arguments, `scheduler_config`, `job_dir` and `command`. 
The `scheduler_config` is `scheduler` which will be the case for all Atlas job submissions.
The `job_dir` refers to the project directory which is `.` and `command` in this case is `main.py`. 
`command` refers to the Docker command to run inside the worker container. We can pass add additional arguments to `command` in case our script accepts command-line arguments. Please refer to the CLI documentation for additional details on the `foundations submit` command.

### Adding project requirements
The Atlas Worker is based on the official [tensorflow image](https://hub.docker.com/layers/tensorflow/tensorflow/1.13.2-gpu-py3-jupyter/images/sha256-1ff5a56100a03bbad26a819521746ca6cf58ff1ee06f5ce3020cc2ed86961abd) and comes pre-configured with some common dependencies like `scikit-learn` and `xgboost`. 
However, if certain project-specific python packages are required, they can be added by adding a `requirements.txt` to the project directory. The Atlas Worker is configured to install the requirements.txt at start-up.

!!! note 
    The requirements.txt is installed everytime a job is launched. 
    It is recommended to use a [custom Worker](https://dessa-atlas-community-docs.readthedocs-hosted.com/en/latest/atlas-modes/scheduling/#custom-workers) with project requirements pre-installed to avoid the start-up delay.
 
### Hyperparameter searches

Atlas makes it really easy to optimize your model by supporting multi-job execution, as well as allowing you to load parameter values during runtime.
During a hyperparameter search, your jobs are queued in the Scheduler. Atlas also exposes various ways of interacting with the job queue (via the CLI or GUI) 
Furthermore, Atlas automatically tracks the parameter values between different jobs, 

The recommended way to launch a hyperparameter search, we make sure of the `foundation.submit()` function. 
This function is the SDK counter-part of the `foundations submit` CLI command and allows your to programmatically submit a large number of jobs to be executed without tying up your console.

There are two important steps when launching a hyperparameter search:
1. Pass in a `dict` of parameters to `foundations.submit()` using the `params` argument
2. Loading in these parameters in the script passed to to the `command` argument using `foundations.load_parameters()`

Let's go through an example below: 
#### Launching a hyper-parameter search

In this random search example, we specify a few hyper-parameter ranges as a `dict`. These are then passed into `foundation.submit()` as shown below:

**Random Search Example:**
```python
import os
os.environ["FOUNDATIONS_COMMAND_LINE"] = True # Required so that an extra job is not created when launching the hyperparameter search

import foundations
 
param_ranges = {
    "epochs": {
        "min": 5,
        "max": 40,
    },
    "layer_shapes": {
        "min": 256,
        "max": 768,
        "count_min": 1,
        "count_max": 3
    }
    "early_stopping_tolerance": 0.01,
    "batch_size": [64, 128, 1024]
}

for _ in range(5):
    params = some_random_parameter_generator(param_ranges)
    foundations.submit(scheduler_config="scheduler", command=["main.py"], params=params)
```
where, the `some_random_parameter_generator` is an implementation of your choice. 
This will queue up multiple jobs with the scheduler that will be executed sequentially. 
Each of these job directories for these experiments will contain a `foundations_job_parameters.json` file that is generated by `foundations.submit()`.
This parameters file now needs to be loaded up at runtime so that the hyperparameter are available at trainig time.

#### Loading in parameter values
The block below shows a sample `foundations_job_parameters.json` file that is generated for one of the queued jobs.   

**foundations_job_parameters.json file:**
```json
{
    "epochs": 6,
    "batch_size": 64,
    "layer_shapes": [128, 256, 192, 128],
    "early_stopping_tolerance": 0.01,
}
```
Recall that in Scheduling mode, your code is executed inside the Atlas worker execution environment. Therefore, the hyperparemeters need to be loaded up at runtime.
This can be conveniently loaded into the script passed into `command` using the `foundations.load_parameters()` function as shown below:

```python
#Example main.py
import foundations

params = foundations.load_parameters()
...

train_model(params["learning_rate"], params["epochs"])
```

This not only makes it easy to specify a lot of different parameter values in one centralized location, but also makes tracking easier when running multiple jobs.
In addition, by using this function, Atlas will automatically track the parameter values for the job on the GUI and SDK so manual parameter logging using `foundations.log_param()` is not required.

See the [log_param](https://dessa-atlas-community-docs.readthedocs-hosted.com/en/latest/sdk-reference/SDK/#log-parameter) docs for more info.

### Retrieving logs and job archives 
#### Viewing logs
Once we submit a hyper-parameter search, the console will only stream logs related to the launch of the hyperparameter search. 
To view logs associated with the actual job execution, copy the Job UUID from the GUI and use the following CLI command:

` foundations get logs scheduler <job_id>` 

This command will retrieve logs for the given job from the `scheduler` execution environment, which is the default environment for Atlas.

#### Retrieving archives
Now that we've run a few jobs, lets retrieve the archive for one of the jobs and see how Atlas provides us with experiment version control. 
Copy the UUID for one of the jobs from the GUI and execute the following command in the console:
`foundations get job scheduler <job_id>`

This command will retrieve the job bundle from the `scheduler` execution environment, which is the default environment for Atlas.
The job bundle contains the state of the directory at the time the job was executed. 
This creates an audit trail for all experiments and their associated artifacts in case a specific model and its code need to be retrieved.

Please refer to the CLI reference for additional information.
 
### Interacting with Jobs
#### Stopping a running job
A running job can be stopped using:
`foundations stop job scheduler <job_id>`

#### Clearing a job queue
Jobs queued for execution in the scheduler can be cleared using:

`foundations clear-queue scheduler`

*Note:* 

*- This command currently clears the entire scheduler queue and affects all projects*

*- Clearing a job queue does not currently delete the associated job archives.* 
These will need to be cleared manually for now and can be found under `~/.foundations/job_data/`* 

#### Deleting jobs
Jobs can be deleted using the following command:
`foundations delete job scheduler <job_id>`

Only completed or failed jobs can be deleted. Deleting a job removes it from the GUI and deletes the associated job archive. 
*Note: sudo access will be required for deleting jobs, this means that you will be prompted for a password*  

### Job configuration
The job configuration file allows for configuration of job related metadata, execution environments & resources. 
A template `job.config.yaml` is generated when creating a project using the `foundations init <project_name>` command.

The example below shows how to update the job config to enable GPU use, set environment variables and mount additional locations inside the Worker:
```yaml
# Project config #
project_name: 'my-atlas-project'
log_level: INFO

# Worker config #
num_gpus: 1
worker:
  image: us.gcr.io/atlas-ce/worker:latest 

  volumes:
    /my/local/path: 
      bind: /my/container/path 
      mode: rw 

  environment:
    MY_ENV_VAR: MY_VALUE 

```
*Note: Please make sure to respect proper indentation of the YAML file* 

### Custom workers

#### Using the standard Worker as a base

Custom Workers allow for the end-user to create or use customized execution environments. 
The simplest use case for custom Workers is to create a worker pre-populated with a `requirements.txt` to avoid the installation of requirements
at job launch.

There are two steps required to create a custom Worker
1. Worker image creation 
2. Worker specification in `job.config.yaml`

The code block below shows a sample Dockerfile to create a custom Worker.
This image will install project specific requirements after inheriting from the base Atlas worker and will set the entrypoint to Python.
The entrypoint override is recommended since the standard Worker image entrypoint installs any `requirements.txt` present in the project directory.

`Dockerfile`
```
FROM atlas-ce/worker:latest

COPY ./requirements.txt /tmp/requirements.txt

RUN pip install --requirement /tmp/requirements.txt
RUN rm /tmp/requirements.txt

ENTRYPOINT ["python"]
``` 

This image can then be built and tagged using: `docker build . -t myCustomWorker:latest`. This will load the docker image into your local docker registry

To use this image, update `job.config.yaml` as below:
```yaml
worker:
  image: myCustomWorker:latest 
```

#### Using a different image as a base
Atlas also supports using a different image as a base, however, in this case, some SDK specific dependencies must be installed. 
To create a custom Worker using a different base, install the following requirements into the image using the steps above:

```
wheel
request
jsonschema
dill==0.2.8.2
redis==2.10.6
pandas==0.23.3
google-api-python-client==1.7.3
google-auth-httplib2==0.0.3
google-cloud-storage==1.10.0
PyYAML==3.13
pysftp==0.2.8
paramiko==2.4.1
mock==2.0.0
freezegun==0.3.8
boto3==1.9.86
boto==2.49.0
flask-restful==0.3.6
Flask==1.1.0
Werkzeug==0.15.4
Flask-Cors==3.0.6
mkdocs==1.0.4
promise==2.2.1
pyarmor==5.5.6
slackclient==1.3.0
scikit-learn==0.21.3
xgboost==0.90
```

### Submitting to a remote scheduler

Job submission is completely configuration driven, with the default config file — `scheduler.config.yaml` — pointing to your local machine. 
This means that if we run `atlas-server start` on an AWS machine, we can simply change our config file to point to that remote machine and still get almost all of the functionality that we do locally.

#### Config file location

By default, the Atlas installer puts all of it's core files under `~/.foundations`, so this documentation assumes this as the root directory of all Atlas files.

The directory `~/.foundations/config/submission` will contain any submission config that you have. You can also run `foundations info --env` to see a list of configs in this location.

From a fresh install, you can note that there is only one. It has the "env_name" of `scheduler`, which is what you use in almost all CLI commands.

#### Creating a custom config file

To add a config to submit to a remote scheduler, we simply need to know the address of the machine and the path to **the remote scheduler's** foundations home directory (`~/.foundations`).

For example, if we create a file at `~/.foundations/config/submission/aws.config.yaml` with the content below:

```yaml
cache_config:
  end_point: /cache_end_point
container_config_root: /<path_to>/.foundations/config/local_docker_scheduler/worker_config
job_deployment_env: local_docker_scheduler_plugin
job_results_root: /<path_to>/.foundations/job_data
scheduler_url: http://<remote_address>:5000
working_dir_root: /<path_to>/.foundations/local_docker_scheduler/work_dir
```

!!! note
    Specifically, you can see that we only need to change the values between `< >` in the following fields:
    
     - container_config_root
     - job_results_root
     - scheduler_url
     - working_dir_root
     
We can now use `aws` as a scheduler config in the CLI or SDK.

Examples:

 - `foundations submit aws . main.py`
 - `foundations.submit(scheduler_config='aws')`
 - `foundations get logs aws <job_id>`
 
!!! warning
    The main missing feature that you will notice is the fact that when running `foundations submit`, you will not get back streaming logs in the CLI. Other than that, everything should be ready to go!
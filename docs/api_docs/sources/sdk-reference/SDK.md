<h1>SDK Reference</h1>

## Log parameter

Logs an individual input parameter when it is called. Logged parameters are accessible programmatically or through the GUI as soon as this function is called within your job.

**Python**

```python
foundations.log_param(key, value)
```

__Arguments__

- __key__ (str): The name of the input parameter.

- __value__ (number, str, bool, array of [number|str|bool], array of array of [number|str|bool]): the value associated with the given input parameter.

__Returns__

- This function doesn't return a value.

__Raises__

- __TypeError__: When a value of a non-supported type is provided as the metric value.

__Note__

Multiple calls with the same key during the same job will overwrite the previously logged value.

__Example__

```python
import foundations
foundations.log_param("learning rate", 0.001)
```

## Log parameter dictionary

Similar to [log_param](#log-parameter), but accepts a dictionary of key-value pairs.

**Python**

```python
foundations.log_params({})
```

__Arguments__

- __dict__ : Dictionary of parameters to log. Each key-value pair needs to satisfy the same constraints as that of [log_param](#log_parameter)

__Raises__

- __TypeError__: When a value of a non-supported type is provided as the metric value.

__Returns__

- This function doesn't return a value.

__Example__

```python
import foundations
foundations.log_params({"learning_rate": 0.001,
                        "batch_size": 32,
                        "epochs": 75})
```

## Log metric

Logs a metric when it is called. Logged metrics are accessible programmatically or through GUI as soon as this function is called within your job.
e.g. this can happen at the end of every epoch to get updated metrics live.

!!! note 
    Currently logging numpy types is not supported.

```python
foundations.log_metric(key, value)
```

__Arguments__

- __key__ (str): the name of the output metric.

- __value__ (number, str, bool, array of [number|str|bool], array of array of [number|str|bool]): the value associated with the given output metric.

__Returns__

- This function doesn't return a value.

__Raises__

- __TypeError__: When a value of a non-supported type is provided as the metric value.

__Note__

Multiple calls with the same key during the same job will create and append to a list containing the previously logged values.

__Example__

```python
import foundations
foundations.log_metric("accuracy", 0.90)
foundations.log_metric("accuracy", 0.93)
```

## Set tag

Sets a tag when it is called. Tags accessible programmatically or through GUI as soon as this line runs within your job. Job tags can also be modified within the GUI.

```python
foundations.set_tag(key)
```

__Arguments__

- __key__ ([number|str]): the name of the tag, displayed on the GUI

__Returns__

- This function doesn't return a value.

__Raises__

- __TypeError__: When a value of a non-supported type is provided as the tag value.

__Example__

```python
import foundations
foundations.set_tag("CNN")
```

## Save artifact
Logs an artifact to a job when called. Artifacts can be images, audio clips, text files or serialized python objects. The artifact must be saved to disk first

```python
foundations.save_artifact(filepath, key)
```

__Arguments__

- __filepath__ ([str]): path of the artifact saved to disk that needs to be logged

- __key__ ([number|str]): friendly name associated with the artifact

__Returns__

- This function doesn't return a value.

__Notes__

Artifacts must be saved to disk before logging.

__Example__

```python
import foundations
foundations.save_artifact("train_val_loss.png", "Loss_Curve")
```

## Job submission
Submits a job to the Atlas Scheduler. 

__Arguments__

- __scheduler_config__ ([str]): Name of the scheduler. Should always be `scheduler` for Atlas

- __job_directory__ ([str]): Default `cwd`. Optional argument to specify job directory

- __project_name__ ([str]): Defaults to current working directory. Optional argument to specify project name. This will take precedence over `job.config.yaml`

- __entrypoint__ ([str]): Optional argument to override the Docker entrypoint of the worker container

- __command__ ([list of str]): List of commands to pass to worker. Typically `['main.py', 'arg1', 'arg2']`

- __num_gpus__ ([int]): Default `0`. Used to set whether to run the worker with GPU support. Any positive number other than 0 will mount all available GPU devices inside the worker

- __params__ ([dict]): Optional argument. Allows you specify parameters for a job. This should be done in JSON serializable dictionary, where values must be supported by `foundations.load_parameters()`. Upon calling `load_parameters()` within job, this param argument will be returned to that job process. See `load_parameters()` docs for loading in parameters.

- __stream_job_logs__ ([bool]): Default `True`. Optional argument to specify if logs should be streamed to the console 


__Returns__

- __deployment__ (Object) -- A deployment object which can be used to interact with the job

__Notes__

The project `requirements.txt` will not be automatically installed if the worker `entrypoint` is overridden using `submit`, please see `Custom workers` docs for more details.

__Example__

```python
import foundations
foundations.submit(scheduler_config="scheduler",
                    command= ["main.py", "myarg1", "myarg2"],
                    num_gpus=1,
                    stream_job_logs=False)
```

#### BETA: Deployment Object

The object returned by `job_deployment = foundations.submit(...)` contains information about the job that it just launched. **In it's current form, there are 3 supported functions.**

```python
# Get back a specific parameter for the job
job_deployment.get_param(param_name: str) -> str
```

```python
# Get back a specific metric for the job
job_deployment.get_metric(metric_name: str) -> str
```

```python
# Get back a dictionary that contains the information stored in the jobs row on the GUI
job_deployment.get_job_details() -> dict
```

!!! note
    All of the calls are blocking. This means that if you call it on a job that is not finished, the function call will wait until the job to finish.
    
!!! warning
    For hyperparameter search, we normally recommend setting the `FOUNDATIONS_COMMAND_LINE` environment variable to `True` to make sure that the search script does not run as a job. **However**,
    for the job deployment object to work it needs this environment variable to be either set to `False` or not set at all. 
    
    This means that your search script will show up as a job in the GUI. This "job" will run as long as the search script takes and act strangly within the GUI (e.g. no logs will appear).
    
    We are aware of this annoyance and have a fix in the works!


## Get project metrics
Retrieve metadata, hyper-parameters, metrics & tags for all jobs associated with a project 

```python
foundations.get_metrics_for_all_jobs(project_name, include_input_params=False)
```

__Arguments__

- __project_name__ ([str]): Name of the project to filter by

- __include_input_params__ ([bool]): Default `False`. Optional way to specify if metrics should include all model input metrics

__Returns__

- __metrics__ (DataFrame) -- A Pandas DataFrame containing all of the results

__Raises__

- __ValueError__ -- An exception indicating that the requested project does not exist

__Notes__

Artifacts must be saved to disk before logging.

__Example__

```python
import foundations
foundations.get_metrics_for_all_jobs("my_project")
```

## Load parameters

Loads job parameters from a file called foundations_job_parameters.json that must exist in the root of the project as a dictionary. This will also log all loaded parameters in the GUI by default.

```python
foundations.load_parameters(log_parameters=True)
```

__Arguments__

- __log_parameters__ (bool): Default `True`. Optional way to specify whether or not to log all parameter values in the GUI and SDK for the job.

__Returns__

- __parameters__ (dict): A dictionary of all the user-defined parameters for the model, from foundations_job_parameters.json.

__Raises__

- __FileNotFoundError__: When the foundations_job_parameters.json file is not found in the deployment directory.

__Example__

Sample `foundations_job_parameters.json`:
```json
{
    "learning_rate": 0.125,
    "layers": [
        {
            "neurons": 5
        },
        {
            "neurons": 6
        }
    ]
}
```
```python
params = foundations.load_parameters()
```

## Syncable directories

Foundations offers an interface to sync a directory within a job to a centralized location outside of that job. This directory can then be synced from a different job,
allowing you to grab information from past jobs to know what has happened in before or build on the shoulders of giants (with giants being your own previous work).

This feature will be useful for advanced model search algorithms that the user may want to do, especially paired with jobs launching other jobs. The synced directories
can be used to quickly achieve genetic search algoritms or Bayesian optimization.

```python
foundations.artifacts.create_syncable_directory(key, directory_path=None, source_job_id=None)
```

__Arguments__

- __key__ (str): What your directory is called in the centralized location.

- __directory_path__ (str): Default `None`. The path to the directory within your jobs environment.

- __source_job_id__ (str): Default `None`. The ID of a previous job that has a directory by the same name as the value given to "key". If this is not specified, the current
job ID is used.

__Returns__

- __syncable_directory__ (SyncableDirectory):

__Examples__


The following example shows how you can create and write to a syncable directory from within a job, and then read and write to the same directory from following jobs.

```python
import foundations
import pandas as pd

df = pd.DataFrame([[1, 2, 3]])

directory = foundations.create_syncable_directory("directory_key", "sync/path")
df.to_csv("sync/path/hello.csv")
directory.upload()
```

If the job gives back the job ID *42*, you can use this to read the saved files from any following job.

```python
import foundations
import pandas as pd

directory = foundations.create_syncable_directory("directory_key", "sync/path", "42")
df = pd.read_csv("sync/path/hello.csv")
```

If you want to write back to the same directory, do so the same way that you did in the first job.

```python
import foundations
import pandas as pd

directory = foundations.create_syncable_directory("directory_key", "sync/path", "42")
df = pd.read_csv("sync/path/hello.csv")

new_df = df + 3
new_df.to_csv("sync/path/hello.csv")
directory.upload()
```

> NOTE: To access the the directory that a job uploaded to, in the state that you expect, always use that job's ID. Example: If you have 5 jobs that all read and write to
a syncable directory with the same key, always use the previous job's ID.

## Syncing Tensorboard log directory

An extra special form of a syncable directory provides the ability to sync a regular Tensorboard logdir to a centralized storage location. Doing this not only allows you to retrieve
files later while tying them to a specific job, but also automatically adds a tag to the job for you. Any job that has this tag can be sent to a Tensorboard server directly from the GUI.

```python
foundations.set_tensorboard_logdir(path)
``` 

__Arguments__

- __path__ (str): The path to your Tensorboard logdir within the jobs environment.

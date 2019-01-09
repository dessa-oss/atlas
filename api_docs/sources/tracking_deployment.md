<h1>Tracking a deployment</h1>
The following methods are members of the deployment object returned when the **run()** method of a stage is called.

----

<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/deployment_wrapper.py#L21)</span>

### job_name


```python
job_name(self)
```



Gets the name of the job being run.

__Arguments__

- This method doesn't receive any arguments.

__Returns__

- __job_name__ (string): The name of the job being run.

__Raises__

- This method doesn't raise any exception.


----

<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/deployment_wrapper.py#L37)</span>

### is_job_complete


```python
is_job_complete(self)
```



Returns whether the job being run has completed.

__Arguments__

- This method doesn't receive any arguments.

__Returns__

- __is_job_complete__ (boolean): True if the job is done, False otherwise (regardless of success / failure).

__Raises__

- This method doesn't raise any exception.


----

<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/deployment_wrapper.py#L53)</span>

### fetch_job_results


```python
fetch_job_results(self, wait_seconds=5)
```



Waits for the job to complete and then fetches the results for the job.
It checks the status of the job periodically to test for completion.

__Arguments__

- __wait_seconds__ (float): The number of seconds to wait between job status check attempts (defaults to 5).

__Returns__

- __results_dict__ (dict): Dict containing results for the stages. See a description below in Notes.

__Raises__

- __RemoteException__: In the event of an exception thrown in the execution environment.

__Notes__

A job is completed when it finishes running due to success or failure. This method will wait for
any of these events to occur. It's a user responsibility to ensure his job is not programmed in a
way that makes it run forever.

The *results_dict* has three keys: *provenance*, *global_stage_context* and *stage_contexts*.
The value of *provenance* is an object that contains internal information about the execution
environment.

The *global_stage_context* value is a dictionary containing the following keys and respective values.

- *uuid*: the universally unique identifier that identifies this stage
- *stage_log*: log information about this stage
- *meta_data*: metadata associated to this stage
- *data_uuid*: the universally unique identifier that identifies data associated to this stage
- *stage_output*: the stage output
- *error_information*: any error information associated to this stage
- *start_time*: the time at which this stage started execution
- *end_time*: the time at which this stage finished execution
- *delta_time*: the time difference between *end_time* and *start_time*
- *is_context_aware*: if this stage is context aware
- *used_cache*: if the stage is using cache
- *cache_uuid*: the universally unique identifier that identifies this stage cache
- *cache_read_time*: the time at which the cache was read
- *cache_write_time*: the time at which the cache was written
- *has_stage_output*: if the stage has output.

The *stage_contexts* value is a dictionary in which each key is a UUID identifiying the stages
upon which this stage depends on. Each value associated to these keys correspond to the
*global_stage_context* of the corresponding stage.


----

<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/deployment_wrapper.py#L107)</span>

### wait_for_deployment_to_complete


```python
wait_for_deployment_to_complete(self, wait_seconds=5)
```



Waits for the job to complete. It checks the status of the job periodically to test for completion.

__Arguments__

- __wait_seconds__ (float): The number of seconds to wait between job status check attempts (defaults to 5).

__Returns__

- This method doesn't return a value.

__Raises__

- This method doesn't raise any exception.

__Notes__

A job is completed when it finishes running due to success or failure. This method will wait for
any of these events to occur. It's a user responsibility to ensure his job is not programmed in a
way that makes it run forever.


----

<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/deployment_wrapper.py#L137)</span>

### get_job_status


```python
get_job_status(self)
```



Similar to is_job_complete, but with more information.

__Arguments__

- This method doesn't receive any arguments.

__Returns__

- __status__ (string): String, which is either "Queued", "Running", "Completed", or "Error".

__Raises__

- This method doesn't raise any exception.



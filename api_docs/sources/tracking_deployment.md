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

__Arguments__

- __wait_seconds__ (float): The number of seconds to wait between job status check attempts (defaults to 5).

__Returns__

- __results_dict__ (dictionary): Dict representing a more-or-less "serialized" PipelineContext for the job.

__Raises__

- __RemoteException__: In the event of an exception thrown in the execution environment.


----

<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/deployment_wrapper.py#L75)</span>

### wait_for_deployment_to_complete


```python
wait_for_deployment_to_complete(self, wait_seconds=5)
```



Waits for the job to complete.

__Arguments__

- __wait_seconds__ (float): The number of seconds to wait between job status check attempts (defaults to 5).

__Returns__

- This method doesn't return a value.

__Raises__

- This method doesn't raise any exception.


----

<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/deployment_wrapper.py#L100)</span>

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



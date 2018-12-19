<h1>Tracking a deployment</h1>
After deploying the code into the execution environment, user's code can track a deployment through the **DeploymentWrapper** instance returned by the **run()** method of a **StageConnectorWrapper** instance.
<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/deployment_wrapper.py#L9)</span>
### DeploymentWrapper

```python
foundations.deployment_wrapper.DeploymentWrapper(deployment)
```

Provides user-facing functionality to deployment classes created through integrations (e.g. LocalShellJobDeployment, GCPJobDeployment)
Arguments:
	deployment: {*JobDeployment} -- The integration-level job deployment to wrap

----

<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/deployment_wrapper.py#L18)</span>

### job_name


```python
job_name(self)
```


Gets the name of the job being run

Returns:
job_name -- The name of the job being run

----

<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/deployment_wrapper.py#L27)</span>

### is_job_complete


```python
is_job_complete(self)
```


Returns whether the job being run has completed

Returns:
is_job_complete -- Boolean value - True if the job is done, False otherwise (regardless of success / failure)

----

<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/deployment_wrapper.py#L36)</span>

### fetch_job_results


```python
fetch_job_results(self, wait_seconds=5)
```


Waits for the job to complete and then fetches the results for the job

Arguments:
	wait_seconds: {float} -- The number of seconds to wait between job status check attempts (defaults to 5)
	verbose_errors: {bool} -- Whether to output stack trace entries relating to Foundations in the event of an exception (defaults to False)

Returns:
results_dict -- Dict representing a more-or-less "serialized" PipelineContext for the job.  Will raise a RemoteException in the event of an exception thrown in the execution environment

----

<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/deployment_wrapper.py#L55)</span>

### wait_for_deployment_to_complete


```python
wait_for_deployment_to_complete(self, wait_seconds=5)
```


Waits for the job to complete

Arguments:
	wait_seconds: {float} -- The number of seconds to wait between job status check attempts (defaults to 5)

----

<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/deployment_wrapper.py#L73)</span>

### get_job_status


```python
get_job_status(self)
```


Similar to is_job_complete, but with more information

Returns:
status -- String, which is either "Queued", "Running", "Completed", or "Error"



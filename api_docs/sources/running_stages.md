<h1>Running stages</h1>
The following methods are members of the stage object returned when a callable returned by **create_stage()** is called.

----

<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/stage_connector_wrapper.py#L84)</span>

### run


```python
run(self, params_dict=None, job_name=None)
```



Deploys and runs the current stage and the stages on which it depends in the configured execution
environment, creating a new job.

__Arguments__

- __params_dict__ (dictionary): optional dictionary of extra parameters to pass the job that would be created.
- __job_name__ (string): optional name for the job that would be created.
- __kw_params__ (keyword arguments): any other optional paramater to pass to the job.

__Returns__

- __deployment__ (DeploymentWrapper): An object that allows tracking the deployment.

__Raises__

- __TypeError__: When an unsupported type is passed to a user function.

__Notes__

The new job runs asynchronously, the current process can continue execution.


----

<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/stage_connector_wrapper.py#L57)</span>

### enable_caching


```python
enable_caching(self)
```



Activates caching of all input parameters for this stage.

__Arguments__

- This method doesn't receive any argument.

__Returns__

- __stage object__: The same object to which this method belongs.

__Raises__

- This method normally doesn't raise exceptions.

__Notes__

At this moment only input parameters that are return values of other stages are cached.



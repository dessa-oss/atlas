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

- __TypeError__: When the type of an argument passed to the function wrapped by this stage is not supported.

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


----

<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/stage_connector_wrapper.py#L145)</span>

### split


```python
split(self, num_children)
```



When a function is wrapped in a stage and it has more than one return value (the return value
is a sequence), the wrapping stage cannot obtain how many values are contained in the returned
sequence due to language contrains. This method allows to specify the number of children values
and splits the result in a corresponding sequence of stages that can be pass forward.

__Arguments__

- __num_children__ (int): number of children values contained in the stage result.

__Returns__

- __children_stages__ (sequence): A sequence of children stages.

__Raises__

- __TypeError__: If the current stage does not contain a sequence of values.
- __IndexError__: If the number of children values is less than __num_children__.



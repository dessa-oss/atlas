<h1>Running stages</h1>
After calling **create_stage()** a callable object &mdash; with the same arguments as the wrapped function &mdash; is returned. When this object is called &mdash; in the same way as the wrapped function would be called &mdash; the user receives a stage object as a result that can be passed further. The following methods are members of this stage object.

----

<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/stage_connector_wrapper.py#L81)</span>

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



Activates caching of the result of current stage and any other stages that it depends on.

__Arguments__

- This method doesn't receive any arguments.

__Returns__

- __stage object__: The same object to which this method belongs.

__Raises__

- This method doesn't raise exceptions.


----

<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/stage_connector_wrapper.py#L142)</span>

### split


```python
split(self, num_children)
```



When a function is wrapped in a stage and it has more than one return value (the return value
is a sequence), the wrapping stage cannot obtain how many values are contained in the returned
sequence due to language constraints. This method allows to specify the number of children values
and splits the result in a corresponding sequence of stages that can be passed forward.

__Arguments__

- __num_children__ (int): number of children values contained in the stage result.

__Returns__

- __children_stages__ (sequence): A sequence of children stages.

__Raises__

- __TypeError__: If the current stage does not contain a sequence of values.
- __IndexError__: If the number of children values is less than __num_children__.



<h1>Running stages</h1>
Once the user has stages defined, it's time to run them in the execution environment. Functions decorated with **create_stage()** return the class **StageConnectorWrapper** which provides the way to deploy user's code to the execution environment and run stages.
<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/stage_connector_wrapper.py#L13)</span>
### StageConnectorWrapper

```python
foundations.stage_connector_wrapper.StageConnectorWrapper(stage, pipeline_context, stage_context, stage_config)
```

----

<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/stage_connector_wrapper.py#L69)</span>

### run


```python
run(self, params_dict=None, job_name=None)
```



Deploys and runs the current stage and the stages on which it depends in the configured execution
environment, creating a new job in the process.

__Arguments__

- __params_dict__ (dictionary): parameters?.
- __job_name__ (string): the name of the job that would be created.
- __kw_params__ (extra keyword arguments): more params?.

----

<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/stage_connector_wrapper.py#L54)</span>

### enable_caching


```python
enable_caching(self)
```



Activates caching of all input parameters for this stage.


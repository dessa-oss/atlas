<h1>Running stages</h1>
<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/stage_connector_wrapper.py#L13)</span>
### StageConnectorWrapper

```python
foundations.stage_connector_wrapper.StageConnectorWrapper(stage, pipeline_context, stage_context, stage_config)
```


User-facing class representing stages on Foundations.

__Arguments__

- __stage__ (StageConnector):  the underlying stage object.
- __pipeline_context__ (PipelineContext): the pipeline context where this stage is going to be run.
- __stage_context__ (StageContext): context information for the stage.
- __stage_config__ (StageConfig): configuration information for the stage.


----

<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/stage_connector_wrapper.py#L78)</span>

### run


```python
run(self, params_dict=None, job_name=None)
```



Deploys and runs the current stage and the stages on which it depends in the configured execution
environment, creating a new job in the process.

__Arguments__

- __params_dict__ (dictionary): optional dictionary of extra parameters to pass the job that would be created.
- __job_name__ (string): optional name for the job that would be created.
- __kw_params__ (keyword arguments): any other optional paramater to pass to the job.


----

<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/stage_connector_wrapper.py#L63)</span>

### enable_caching


```python
enable_caching(self)
```



Activates caching of all input parameters for this stage.



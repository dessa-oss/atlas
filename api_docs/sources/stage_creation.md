<h1>Creating stages</h1>
When using Foundations, the user divides their Machine Learning solution into stages, each one representing a step in the process. Each stage is written as a function that must me decorated with Foundations's **create_stage()** function.
<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/staging.py#L9)</span>

### create_stage


```python
create_stage(function)
```



Transforms any Python function into a callable that represents a stage in Foundations.

__Arguments__

- __function__ (callable): Function to wrap.

__Returns__

- __stage_generator__ (callable): A callable that when executed returns a stage object.



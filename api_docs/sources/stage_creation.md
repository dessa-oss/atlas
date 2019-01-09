<h1>Stage creation</h1>
<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/staging.py#L9)</span>

### create_stage


```python
create_stage(function)
```



Given a Python function, returns a callable with the same signature (receiving the same arguments) as the
wrapped function which can be called in the same way as the wrapped function but will create a stage
in Foundations instead.

__Arguments__

- __function__ (callable): Function to wrap.

__Returns__

- __stage_generator__ (callable): A callable that when executed returns a stage object.

__Raises__

- This function doesn't raise exceptions.



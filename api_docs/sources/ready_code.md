<h1>Log metrics</h1>
<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/stage_logging.py#L14)</span>

### log_metric


```python
log_metric(key, value)
```



Log metrics within a stage from where it is called.

__Arguments__

- __key__ (string): the name of the output metric.
- __value__ (number, str, bool, array of base types, array of array of base types): the value associated with the given output metric.

__Returns__

- __Nothing__ (None).

__Raises__

- __TypeError__: When a value of a non-supported type is provided as the metric value.

__Notes__

A stage containing this function won't fail if this function fails.



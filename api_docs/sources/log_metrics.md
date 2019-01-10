<h1>Log metrics</h1>
<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/stage_logging.py#L14)</span>

### log_metric


```python
log_metric(key, value)
```



Log metrics within a stage from where it is called.

__Arguments__

- __key__ (str): the name of the output metric.
- __value__ (number, str, bool, array of [number|str|bool], array of array of [number|str|bool]): the value associated with the given output metric.

__Returns__

- This function doesn't return a value.

__Raises__

- __TypeError__: When a value of a non-supported type is provided as the metric value.

__Notes__

A stage containing this function will not fail if the process of logging the metric fails for a
reason that doesn't raise any exceptions.

__Example__

```python
import foundations
from algorithms import calculate_score

def my_stage_code(self):
    score = calculate_score()
    foundations.log_metric('score', score)
```



<h1>Stage creation</h1>
<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/staging.py#L9)</span>

### create_stage


```python
create_stage(function)
```



Takes a Python function as argument and returns a callable with the same signature (receiving the same
arguments) as the input function. The returned callable can be called in the same way as the input
function but will create a stage in Foundations instead. Wrapping a function as a stage makes it
possible for Foundations to track calls, inputs and outputs of the function.

__Arguments__

- __function__ (callable): Function to wrap.

__Returns__

- __stage_generator__ (callable): A callable that when executed returns a stage object.

__Raises__

- This function doesn't raise exceptions.

__Example__

```python
import foundations
from data_helper import load_data
from algorithms import train_model

load_data = foundations.create_stage(load_data)
train_model = foundations.create_stage(train_model)
data = load_data()
model = train_model(data)
model.run()
```



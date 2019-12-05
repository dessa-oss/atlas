<h1>Hyperparameters</h1>
The Hyperparameter class can be used to define hyperparameters which are configuration values that are external to the model and cannot be estimated from data. With Foundations, hyperparameters have values generated during runtime for experimentation and can help identify the optimal model

---
<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/hyperparameter.py#L14)</span>

### __Hyperparameter__


```python
Hyperparameter(self, name=None)
```

Creates a Hyperparameter object which, when passed into a stage, has its value dynamically generated during runtime. This is used to optimize models

__Arguments__

- __name__ (string): The name of the hyperparameter for tracking on the GUI or getting results, used for model management 

__Example__

```python
import foundations
from algorithms import train_model

train_model = foundations.create_stage(train_model)
data1 = foundations.Hyperparameter('rate')
model = train_model(data1)
model.run(job_name='Experiment number 2', params_dict={data1: 0.2})
```
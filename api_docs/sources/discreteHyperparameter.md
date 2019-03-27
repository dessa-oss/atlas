<h1>Additional Hyperparameter Classes</h1>
The following classes can be used to define structured ways of specifying different Hyperparameter values which Foundations will iterate through during runtime. 

**NOTE:** These features are **EXPERIMENTAL** and may be subject to change in future releases.  

---
<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/discrete_hyperparameter.py#L14)</span>

### __DiscreteHyperparameter__


```python
DiscreteHyperparameter(self, values)
```

Creates a DiscreteHyperparameter object which holds an internal list of possible values for hyperparameter substitution.

__Arguments__

- __values__ (list): The list of numeric values to use for hyperparameter substitution.

__Example__

```python
import foundations
from algorithms import train_model

train_model = foundations.create_stage(train_model)
model = train_model(data1=foundations.Hyperparameter())
model.grid_search(
    params_dict={'data1': foundations.DiscreteHyperparameter([0.25, 0.125, 1.0])})
```
---
<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/floating_hyperparameter.py#L14)</span>

### __FloatingHyperparameter__


```python
FloatingHyperparameter(self, min, max, step=None)
```
Creates a new FloatingHyperparameter object used for an analogue of range() for floats in the case of grid search,
        and a uniform distribution in the case of random search

__Arguments__

- __min__ (float): Left end of uniform distribution. Included in searching
- __max__ (float): Right end of uniform distribution. Included in searching
- __step__ (float): Grid size for grid search - think range(min, max, step), where max is actually included. Defaults to None (useful for random search)

__Example__

```python
import foundations
from algorithms import train_model

train_model = foundations.create_stage(train_model)
model = train_model(data1=foundations.Hyperparameter())
model.grid_search(
    params_dict={'data1': foundations.FloatingHyperparameter(0.25, 1, 0.25)})
```
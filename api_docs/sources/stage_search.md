<h1>Hyperparameter Searching</h1>
The following methods are used to perform Hyperparameter tuning/search without having to write additional loops or code to iterate over a distribution

**NOTE:** These features are **EXPERIMENTAL** and may be subject to change in future releases.  


----

<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/stage_connector_wrapper.py#L243)</span>

### random_search


```python
random_search(self, params_range_dict, max_iterations)
```



Calls .run() with random combinations of the hyperparameters used and evaluates each model.

__Arguments__

- __params_range_dict__ (dict): a dictionary containing FloatingHyperparameter or DiscreteHyperparameter objects.
- __max_iterations__ (int): parameter to specify number of total loops to run.

__Returns__

- __deployments__ (dict): a dictionary containing individual deployment objects mapped by job_id.

__Raises__

- __    TypeError__: When the type of an argument passed to the function wrapped by this stage is not supported.

__Example__

```python
import foundations
from algorithms import train_model

train_model = foundations.create_stage(train_model)
model = train_model(data1=foundations.Hyperparameter())
model.random_search(job_name='Experiment number 2', 
	params_dict={'data1': foundations.FloatingHyperparameter(0.25, 1, 0.025)})
```


----

<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/stage_connector_wrapper.py#L274)</span>

### grid_search


```python
grid_search(self, params_range_dict, max_iterations=None)
```



Calls .run() for every combination of hyperparameters specified and evaluates each model.

__Arguments__

- __params_range_dict__ (dict): a dictionary containing FloatingHyperparameter or DiscreteHyperparameter objects.
- __max_iterations__ (int): optional parameter to specify number of total loops to run, none by default.
which will loop through every combination.

__Returns__

- __deployments__ (dict): a dictionary containing individual deployment objects mapped by job_id.

__Raises__

- __    TypeError__: When the type of an argument passed to the function wrapped by this stage is not supported.

__Example__

```python
import foundations
from algorithms import train_model

train_model = foundations.create_stage(train_model)
model = train_model(data1=foundations.Hyperparameter())
model.grid_search(job_name='Experiment number 2', 
	params_dict={'data1': foundations.DiscreteHyperparameter([0.25, 0.125, 1.0])})
```




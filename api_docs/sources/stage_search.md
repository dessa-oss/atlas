<h1>Hyperparameter Searching</h1>
The following methods are used to perform Hyperparameter tuning/search without having to write additional loops or code to iterate over a distribution. There are currently two available search types:

**Grid Search**: A technique typically used to find the optimal set of hyperparameters for a particular model. In Foundations, grid searching is automatically handled by deploying individal jobs for each *exact combination* of input Hyperparameter values. For example, if there are 2 Hyperparameters with 3 values each, Foundations will deploy 9 jobs and evaluate the model for each of the given Hyperparameter values. 

**Random Search**: A technique used where random combinations of the hyperparameters are assessed to find the best solution for the built model. With Foundations, random searching is automatically done by deploying indvidual jobs for random combinations of input Hyperparameter values. For example, if there are 2 Hyperparameters with 3 values each, Foundations will *randomly* pick combinations for each Hyperparameter of those values up to a specificed maximum number of iterations. 

**NOTE:** These features are **EXPERIMENTAL** and may be subject to change in future releases.  


----

<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/stage_connector_wrapper.py#L243)</span>

### random_search


```python
random_search(self, params_range_dict, max_iterations)
```



Replaces the .run() call on a stage and launches multiple jobs with random combinations of the hyperparameters passed in.

__Arguments__

- __params_range_dict__ (dict): a dictionary containing FloatingHyperparameter or DiscreteHyperparameter objects.
- __max_iterations__ (int): parameter to specify number of total loops to run.

__Returns__

- __deployments__ (dict): a dictionary containing individual deployment objects mapped by job_id.

__Raises__

- __    ValueError__: When the value of a Hyperparameter passed into the function is not iterable.
- __    AttributeError__: When the dictionary passed in does not contain a Hyperparameter object.
- __    TypeError__: When the type of an argument passed to the function wrapped by this stage is not supported.

__Example__

```python
import foundations
from algorithms import train_model

foundations.set_project_name('random_search_example')
train_model = foundations.create_stage(train_model)
model = train_model(data1=foundations.Hyperparameter())

# Launches 5 jobs where random values between 0.25 and 1 at increments of 0.025 are selected
# Ex: 5 independent jobs where the data1 values are (0.25, 0.55, 0.425, 0.7, 0.325)
model.random_search( 
	params_dict={'data1': foundations.FloatingHyperparameter(0.25, 1, 0.025), 5})

# Results from the 5 jobs can be retrieved with get_metrics_for_all_jobs
print(foundations.get_metrics_for_all_jobs('random_search_example')
```


----

<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/stage_connector_wrapper.py#L283)</span>

### grid_search


```python
grid_search(self, params_range_dict, max_iterations=None)
```



Replaces the .run() call on a stage and launches multiple jobs with every combinations of the hyperparameters passed in.

__Arguments__

- __params_range_dict__ (dict): a dictionary containing FloatingHyperparameter or DiscreteHyperparameter objects.
- __max_iterations__ (int): optional parameter to specify maximum number of total loops to run, none by default which will loop through every possible combination of Hyperparameter values passed in.

__Returns__

- __deployments__ (dict): a dictionary containing individual deployment objects mapped by job_id.

__Raises__

- __    ValueError__: When the value of an Hyperparameter passed into the function is not iterable.
- __    AttributeError__: When the dictionary passed in does not contain a Hyperparameter object.
- __    TypeError__: When the type of an argument passed to the function wrapped by this stage is not supported.

__Example__

```python
import foundations
from algorithms import train_model

foundations.set_project_name('grid_search_example')
train_model = foundations.create_stage(train_model)
model = train_model(data1=foundations.Hyperparameter(), data2=foundations.Hyperparameter())

# Launches 9 jobs where the values of data1 and data2 are the exactly same as the ones defined in the Hyperparameters
# Ex: 9 independent jobs where the data1 values are exactly(0.25, 0.125, 1) 
# for each exact step value of data2 (4, 5, 6) in the distribution
model.grid_search(
	params_dict={'data1': foundations.DiscreteHyperparameter([0.25, 0.125, 1.0]),
		        'data2': foundations.FloatingHyperparameter(4, 6, 1)})

# Results from the 9 jobs can be retrieved with get_metrics_for_all_jobs
print(foundations.get_metrics_for_all_jobs('grid_search_example')
```




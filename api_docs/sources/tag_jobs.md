<h1>Tagging Jobs</h1>
The following methods are used to add additional information to jobs for experiment management, giving users the flexibility to 
provide as much detail as a job as needed

**NOTE:** These features are **EXPERIMENTAL** and may be subject to change in future releases.  

---
<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/prototype/projects.py#L55)</span>

### set_tag


```python
set_tag(key, value)
```



Adds additional static, predetermined information as a tag to the job. This is a way to categorize attributes of a job that is not dynamically generated during runtime.

__Arguments__

- __key__ (str): the name of the tag.
- __value__ (number, str, bool, array of [number|str|bool], array of array of [number|str|bool]): the value associated with the given tag.

__Returns__

- This function doesn't return a value.

__Raises__

- This method doesn't raise any exceptions.

__Notes__

If a tag is updated multiple times, Foundations will update the tag to the newest value, but return a warning indicating that the
key has been updated.

__Example__

```python
import foundations
import foundations.prototype
from algorithms import train_model_xgboost

train_model = foundations.create_stage(train_model_xgboost)
model = train_model()
foundations.prototype.set_tag('model', 'xgboost')
model.run()
```


----

<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/prototype/projects.py#L8)</span>

### get_metrics_for_all_jobs


```python
get_metrics_for_all_jobs(project_name)
```



Returns metrics and tags for all jobs for a given project. This function is an experimental feature, and is under the foundations.prototype package.

__Arguments__

- __project_name__ (string): Name of the project to filter by.
- __include_input_params__ (boolean): Optional way to specify if metrics should include all model input metrics.

__Returns__

- __metrics__ (DataFrame): A Pandas DataFrame containing all of the results.

__Raises__

- __ValueError__: An exception indicating that the requested project does not exist.

__Example__

```python
import foundations
import foundations.prototype
from algorithms import train_model, print_metrics

train_model = foundations.create_stage(train_model)
foundations.prototype.set_tag('model', 'CNN')
model = train_model()

all_metrics = foundations.prototype.get_metrics_for_all_jobs(job_name)
print_metrics(all_metrics)
```



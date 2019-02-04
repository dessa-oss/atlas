<h1>Reading job metrics</h1>
<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/projects.py#L14)</span>

### get_metrics_for_all_jobs


```python
get_metrics_for_all_jobs(project_name)
```



Returns metrics for all jobs for a given project.

__Arguments__

- __project_name__ (string): Name of the project to filter by.

__Returns__

- __metrics__ (DataFrame): A Pandas DataFrame containing all of the results.

__Raises__

- __ValueError__: An exception indicating that the requested project does not exist.

__Example__

```python
import foundations
from algorithms import train_model, print_metrics

train_model = foundations.create_stage(train_model)
model = train_model()
job_name = 'Experiment number 3'
deployment = model.run(job_name=job_name)
deployment.wait_for_deployment_to_complete()
all_metrics = foundations.get_metrics_for_all_jobs(job_name)
print_metrics(all_metrics)
```



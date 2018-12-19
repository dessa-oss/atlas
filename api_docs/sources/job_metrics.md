<h1>Getting job metrics</h1>
After running their code, a user can obtain metrics from the job that was run in the remote environment.
<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/projects.py#L14)</span>

### get_metrics_for_all_jobs


```python
get_metrics_for_all_jobs(project_name)
```



Returns metrics for all jobs for a given project.

__Arguments__

- __project_name__ (str): Name of the project to filter by.

__Returns__

A Pandas DataFrame containing all of the results.


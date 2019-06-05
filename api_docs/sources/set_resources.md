<h1>Allocating Resource for Deployments</h1>
The following method(s) is used to specify infrastructure resources for running jobs, if desired. Users should be able to specify the amount of GPUs and RAM they'd like the job to use, in order to speed up or prioritize jobs.

**NOTE:** These features are **EXPERIMENTAL** and may be subject to change in future releases. In addition, this only works for specific version of the Foundations Job orchestrator (scheduler), please confirm with the Dessa integrations team if this will work for your setup.

In addition, using the feature will set resources for the current and future jobs, unless this feature is run again to remove any specific resource allocation.

---
<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations_contrib/set_job_resources.py#L11)</span>

### set_job_resources


```python
set_job_resources(num_gpus, ram)
```



Specifies the resources to run a job with. The available amount will greatly depend on what is available on the infrastrcture that the Foundations job orchestrator is setup on.

__Arguments__

- __num_gpus__ (int): The number of GPUs to run the job with. By default uses 0, indicating the job will run with CPU resources instead.
- __ram__ (number): The amount of ram in GB to use while running the job. Must be greater than 0.

__Returns__

- This function doesn't return a value.

__Raises__

ValueError: If either the RAM or GPU quantity is an invalid value (ex: less than 0) or not specified.

__Notes__

Setting the resources for a job will apply to all future jobs even if the function is not present in the code as it updates the configuration on the orchestrator side. To clear specifying resources and use the default
or CPU resources, you can pass in set_job_resources(0, None).

__Example__

```python
import foundations
from algorithms import train_model

foundations.set_job_resources(1, 1)
train_model = foundations.create_stage(train_model)
model = train_model()
model.run()
```




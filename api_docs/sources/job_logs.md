<h1>Getting Remote Job Logs</h1>
The following method(s) are members of the deployment object returned when the run() method of a stage is called.

**NOTE:** These features are **EXPERIMENTAL** and may be subject to change in future releases.  


----

<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/deployment_wrapper.py#L218)</span>

### get_job_logs


```python
get_job_logs(self)
```



Get stdout log for job deployed with SSH job deployment.

__Arguments__

- This method doesn't receive any arguments.

__Returns__

- __log__ (string): String, which is the contents of the stdout log stream.

__Raises__

- This method doesn't raise any exception.

__Example__

```python
import foundations
from algorithms import train_model

train_model = foundations.create_stage(train_model)
model = train_model()
deployment = model.run()
logs = deployment.get_job_logs()
print('Stdout log:', logs)
```


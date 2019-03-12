<h1>Managing Jobs</h1>
The following methods are used to manage the job queue for deployments and give users maximum flexibility when deploying and organizing experiments.

**NOTE:** These features are **EXPERIMENTAL** and may be subject to change in future releases.  

---
<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/prototype/jobs.py#L8)</span>

### get_queued_jobs


```python
get_queued_jobs()
```



Retrieves all deployed jobs which are in queue to run, but are not currently running.

__Arguments__

- This method doesn't receive any arguments.

__Returns__

- __queued_jobs__ (DataFrame): A Pandas DataFrame containing all of the jobs which are in queue.

__Raises__

- This method doesn't raise any exceptions.

__Example__

```python
import foundations
import foundations.prototype
from algorithms import train_model

train_model = foundations.create_stage(train_model)
model = train_model()
model.run()

job_queue = foundations.prototype.get_queued_jobs()
print(job_queue)
```


----

<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/prototype/jobs.py#L42)</span>

### cancel_queued_jobs


```python
cancel_queued_jobs(list_of_job_ids)
```



Cancels jobs which are currently in the queue, preventing them from eventually running when resources are available.

__Arguments__

- __list_of_job_ids__ (array): a list of job_ids as strings to cancel.

__Returns__

- __cancelled_statuses__ (dict): A dictionary indicating if the cancelling of a queued job was successful or not for each input job_id.

__Raises__

- This method doesn't raise any exceptions.

__Example__

```python
import foundations
import foundations.prototype
from algorithms import train_model

train_model = foundations.create_stage(train_model)
model = train_model()
model.run()

foundations.prototype.get_queued_jobs()
job_queue = foundations.prototype.cancel_queued_jobs(['209762cb-c767-4aea-bcaa-35b131982915'])
print(job_queue)
```


----

<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/prototype/jobs.py#L91)</span>

### cancel_queued_jobs


```python
cancel_queued_jobs(list_of_job_ids)
```



Cancels jobs which are currently in the queue, preventing them from eventually running when resources are available.

__Arguments__

- __list_of_job_ids__ (array): a list of job_ids as strings to cancel.

__Returns__

- __cancelled_statuses__ (dict): A dictionary indicating if the cancelling of a queued job was successful or not for each input job_id.

__Raises__

- This method doesn't raise any exceptions.

__Example__

```python
import foundations
import foundations.prototype
from algorithms import train_model

train_model = foundations.create_stage(train_model)
model = train_model()
model.run()

foundations.prototype.get_queued_jobs()
job_queue = foundations.prototype.cancel_queued_jobs(['209762cb-c767-4aea-bcaa-35b131982915'])
print(job_queue)
```


----

<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/prototype/jobs.py#L91)</span>

### archive_jobs


```python
archive_jobs(list_of_job_ids)
```



Archives completed jobs, removing them from any project results on both the GUI and SDK.

__Arguments__

- __list_of_job_ids__ (array): a list of job_ids as strings to archive.

__Returns__

- __archived_statuses__ (dict): A dictionary indicating if the archiving was successful or not for each input job_id.

__Raises__

- This method doesn't raise any exceptions.

__Example__

```python
import foundations
import foundations.prototype
from algorithms import train_model

foundations.get_metrics_for_all_jobs("Demo_Project")
job_queue = foundations.prototype.archive_jobs(['209762cb-c767-4aea-bcaa-35b131982915'])
print(job_queue)
```



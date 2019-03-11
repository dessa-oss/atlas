<h1>Specifying Project Names For Your Experiments</h1>
<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/projects.py#L9)</span>

### set_project_name


```python
set_project_name(project_name='default')
```



Sets the project a given job. This allows Foundations to know that multiple jobs belong to the same project. The project name is later used to retrieve metrics and analyze experiments.

__Arguments__

- __project_name__ (string): Optional name specifying which project the job is part of. If no project name is specified, the job will be deployed under the "default" project.

__Returns__

- This function doesn't return a value.

__Raises__

- This method doesn't raise any exceptions.

__Example__

```python
import foundations
from algorithms import train_model

foundations.set_project_name("my project")

train_model = foundations.create_stage(train_model)
model = train_model()
deployment = model.run()
```



<h1>Setting Deployment Environment</h1>
<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/config.py#L8)</span>

### set_environment


```python
set_environment(environment_name)
```



Sets the deployment environment where the job is run. Equivalent to specifying --env when deploying through the Foundations CLI.

__Arguments__

- __environment_name__ (string): the name of the deployment environment. Available environments can be displayed with the Foundations CLI command 'foundations info --env'.

__Returns__

- This function doesn't return a value.

__Raises__

- __ValueError__: An exception indicating that the specified environment_name does not exist.

__Notes__

Primarily used when using Jupyter to specify deployment environment without the Foundations CLI.

__Example__

```python
#Jupyter Cell
import foundations
foundations.set_environment('local')

#Jupyter Cell
from project_code.data_helper import load_data
from project_code.algorithms import train_model

load_data = foundations.create_stage(load_data)
train_model = foundations.create_stage(train_model)
data = load_data()
model = train_model(data)
model.run()
```



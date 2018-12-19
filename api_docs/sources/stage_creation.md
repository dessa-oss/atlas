<h1>Creating stages</h1>
When using Foundations, the user divides their Machine Learning solution into stages, each one representing a step in the process. Each stage is written as a function that must me decorated with Foundations's **create_stage()** function.
<span style="float:right;">[[source]](https://github.com/DeepLearnI/foundations/blob/master/foundations/staging.py#L8)</span>

### create_stage


```python
create_stage(function)
```


Take in a function and returns a method capable of generating stages

Arguments:
function {callable} -- Function to wrap

Returns:
callable -- Stage generator


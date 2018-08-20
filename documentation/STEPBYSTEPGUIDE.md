# Step by step Guide

## Step 1: Writing a model code

Consider a naive model which takes an input(x), increases it's value by 10 and then multiples it(x+10) by some value(y) to output result(y * (x+10))

This very naive model code is all under one package.
The example package is [here](https://github.com/DeepLearnI/foundations/documentation/sample_code/models).
This package has a [naive model](https://github.com/DeepLearnI/foundations/documentation/sample_code/models/model.py).

This model consists of two steps:
1. To increase value by 10
2. To multiple this increased value certain number
In the end, this model outputs an multiplied value

We recommend, best coding practices, to break down model code into different small functions(steps). Breaking code into functions is maintainable and re-usable(more on that in next few steps).

## Step 2: Use Foundations to run model code


The [driver.py file](https://github.com/DeepLearnI/foundations/documentation/sample_code/driver.py) shows how to use Foundations to run model code. Lets look at it line by line.

```from foundations import * ```
will import all function from Foundations.

```from staged_models.model import incr_by_10, mult```
Notice, we prefix module name with `staged_`. This wraps imported functions (`incr_by_10, mult`) through Foundations package.

```
# build step1 of model
incr_value = incr_by_10(x)
```
`incr_by_10` function is wrapped through Foundations. This step doesn't execute `incr_by_10` function, it creates a pointer to the first step of the model. When this function is executed the return value from the function is wrapped in an object which is assigned to `incr_value` variable, from here on we call it `stage_object`.

```
# build step2 of model
result = mult(x, incr_value)
```
This behave exactly same as above, `result` is `stage_object`. Notice, we are passing `incr_value` to `mult` function. `incr_value` is a stage_object and has not been executed yet.

```
# run the model
result.run()
```
To execute any stage, we need to invoke `run` function on the stage_object. This step will execute the stage and any dependent stage it needs to invoke.

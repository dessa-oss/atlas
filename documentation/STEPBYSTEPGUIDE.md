# Step by step Guide

## Step 1: Writing a model code

Consider a naive model which takes an input(x), increases it's value by 10 and then multiples it(x+10) by some value(y) to output result(y * (x+10))

This very naive model code is all under one package.
The example package is [here](sample_code).
This package has a [naive model](sample_code/model.py).

This model consists of two steps:
1. To increase value by 10
2. To multiply this increased value by a given number

In the end, this model outputs a multiplied value.

For best coding practices we recommend breaking down model code into different small functions(steps). Structuring code into functions makes for more maintainable and re-usable code in the long run.

## Step 2: Use Foundations to run model code

The [driver.py file](sample_code/driver.py) shows how to use Foundations to run model code. Let's look at it line by line.

```
import foundations
from models.model import incr_by_10, mult
incr_by_10 = foundations.create_stage(incr_by_10)
mult = foundations.create_stage(mult)

`incr_by_10` function is wrapped through Foundations. This step doesn't execute `incr_by_10` function, it creates a pointer to the first step of the model.
Similary,  `mult` function is wrapped through Foundations.

```

# build step1 of model
incr_value = incr_by_10(x)
```
This step doesn't execute `incr_by_10` function, it creates a pointer to the first step of the model. When this function is executed the return value from the function is wrapped in an object which is assigned to `incr_value` variable, from here on we call it `stage_object`.

```
# build step2 of model
result = mult(x, incr_value)
```
This behaves the same as above, `result` is `stage_object`. Notice, we are passing `incr_value` to `mult` function. `incr_value` is a stage_object and has not been executed yet.

```
# run the model
result.run()
```
To execute any stage, we need to invoke `run` function on the stage_object. This step will execute the stage and any dependent stage it needs to invoke.

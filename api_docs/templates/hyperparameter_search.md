<h1>Hyperparameter Tuning on the Titanic Dataset</h1>

**Note:** Is it highly recommended to look at the [logistic regression](../regression/) example before following this example.

In a previous [example](../regression/), we looked at how to use Foundations to build and deploy a logistic regression model. Now, we'll explore hyperparameter tuning with Foundation via grid search. When experimenting with various parameters, you will only need to deploy the job *once*, and Foundations will automatically take care of trying different models with different parameters, as well as tracking the results in a centralized place. We'll also be using [caching](../running_stages/#enable_caching) to help signifigantly reduce model training time.

You will need the files from the logistic regression [example](../regression/), as we will only be modifying the driver.py file. It's also recommended to create a new project with the Foundations CLI [command](../project_creation/#project-creation). The directory structure should look like this to run the model correctly:
```
hyperparameter_example
├── config
│   └── local.config.yaml
├── data
|   └── titanic.csv
├── post_processing
│   └── results.py
├── project_code
│   ├── utilities
|   |   └── data_pipeline.py
|   |   └── logging.py
|   |   └── prep.py
|   |   └── one_hot_encoder.py
|   |   └── encoder_wrapper.py
|   ├── driver.py
│   └── model.py
└── README.txt
```
###Using Hyperparameters

 Typically in model training, you'll have parameters that you'll want to vary across jobs while keeping the basic structure of the model itself the same (e.g. learning rate, number of neurons, etc.). By using a Hyperparameter object instead of an actual value, this creates a placeholder for Foundations to fill during the invocation of `.run()`. Foundations allows supplying arguments to the `.run()` function such as:
 ```python
 stage.run('A'=0.25, 'B'=100)
 ```

---
##Driver File
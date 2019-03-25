<h1>Training a XGBoost Model on the Iris Dataset</h1>

In this example, we will use Foundations and scikit-learn to train a simple XGBoost on the [Iris Flower Dataset](https://scikit-learn.org/stable/auto_examples/datasets/plot_iris_dataset.html) to determine what kind of Iris a flower is based off pedal lengths and widths. We will be leveraging the dataset directly from sklearn, so no download of data is required. 

The workflow of the example will be as follows:  
<span>1. </span> Load the data  
<span>2. </span> Prepare the data  
<span>3. </span> Train the Model  
<span>4. </span> Validation and Results

For best practices, rather than run the whole model in one call, we will divide each step in the model into independent functions, making model development more modular and easier to debug. Foundations will then be used to wrap these functions to perform provenance tracking, caching, prepping your job for deployment, etc.

Some additional python dependencies you will need to install include: `sklearn` `xgboost`

The directory structure should look like this to run the model correctly:
```
xgboost_example
├── config
│   └── local.config.yaml
├── data
├── post_processing
│   └── results.py
├── project_code
|   ├── driver.py
│   └── model.py
└── README.txt
```
For additonal information on how to deploy the model, check out our documentation [here](../configs/#how-to-deploy). 

It is highly recommended to first create a new project using the Foundations CLI [command](../project_creation/#project-creation). The following example code will then go directly into the driver.py and model.py files respectively.

Note: This is **not** a complete course on deep learning. Instead, this tutorial is meant to get you from zero to your first 
model trained with Foundations with as little headache as possible!
---
##1. Load the dataset
First, lets load the dataset we'll be using for this example in the model.py file. Since we'll be using scikit-learn, we'll need to import the dataset as well as a few other dependencies. We've arbitrarily chosen the test/training data split to be 20% of the whole set. We've also selected a random_state of 42. More information on the `train_test_split` function can be found [here](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html):

```python
"""
model.py
"""
import foundations
import numpy as np
import xgboost as xgb
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.datasets import dump_svmlight_file
from sklearn.externals import joblib
from sklearn.metrics import precision_score

def load_data():
	iris = datasets.load_iris()
	X = iris.data
	y = iris.target
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

	return X_train, X_test, y_train, y_test
```

In the driver.py file, we can now create our first stage (or step in the pipeline) for Foundations to manage.

```python
"""
driver.py
"""
import foundations

from model import load_data

# Set a project a name so that Foundations knows how to track the model when it is deployed
foundations.set_project_name("XGBoost Example")

load_data = foundations.create_stage(load_data)

X_train, X_test, y_train, y_test = load_data().split(4)
```
Here, we've turned the `load_data` function into a Foundations stage which returns a callable with the exact same signature as the input `load_data` function. When Foundations runs the pipeline, it will be called in the same way as the input function, but will return a stage object instead which Foundations uses to track inputs and outputs.

Also, notice how we split the dataset above into training and test data. Because of this, when we turn `load_data` into a stage for Foundations to manage, we'll need to use the `.split()` [function](../running_stages/#split) in the driver file so that we correctly capture the number of returned values.  

##2. Prepare the data
Now that we have the data available, we need to create the XgBoost specific DMatrix data format from the numpy array. This can be done with the XgBoost package directly which we'll add to the model.py file: 

```python
"""
model.py
"""
def create_matrix(X_train, X_test, y_train, y_test):
	dtrain = xgb.DMatrix(X_train, label=y_train)
	dtest = xgb.DMatrix(X_test, label=y_test)

	return dtrain, dtest
```
In the driver.py, we can create a stage out of the create_matrix function:  

```python
"""
driver.py
"""
import foundations

from model import load_data, create_matrix

foundations.set_project_name("XGBoost Example")

load_data = foundations.create_stage(load_data)
create_matrix = foundations.create_stage(create_matrix)

X_train, X_test, y_train, y_test = load_data().split(4)

dtrain, dtest = create_matrix(X_train, X_test, y_train, y_test).split(2)
```
Here we pipe the outputs of the `load_data()` stage into the `create_matrix()` stage. Outputs of one stage can be treated as standard variables, and can be used in future stages. Because the `reshape` input function returns 2 values, we need to use `.split()` again to indicated to Foundations how many values are generated from the input function.

##3. Train the model
Now that we have loaded and processed the data, the next step is to run the XgBoost model. In order to run XgBoost, we'll need to pass in some [parameters](https://xgboost.readthedocs.io/en/latest/parameter.html) into the model. For now, we'll define the function to take a dictionary called `param` which the xgboost model will use when training. We also need to indicate the number of iterations we want the tree to run.
```python
"""
model.py
"""
def train_model(param, iterations, training_data, test_data):
	boost = xgb.train(param, training_data, iterations)
	predictions = boost.predict(test_data)

	return predictions
```
In the driver.py file we create a `train_model` stage as the next step in our pipeline after loading and processing the data:
```python
"""
driver.py
"""
import foundations
from model import load_data, create_matrix, train_model

foundations.set_project_name("Xgboost Example")

load_data = foundations.create_stage(load_data)
create_matrix = foundations.create_stage(create_matrix)
train_model = foundations.create_stage(train_model)

#Define model parameters which will likely need tuning and more experimentation to find the ideal parameters
param = {
    'max_depth': 1,  # the maximum depth of each tree
    'eta': 0.3,  # the training step for each iteration
    'silent': 1,  # logging mode - quiet
    'objective': 'multi:softprob',  # error evaluation for multiclass training
    'num_class': 3}  # the number of classes that exist in this datset
num_round = 1  # the number of training iterations

X_train, X_test, y_train, y_test = load_data().split(4)

dtrain, dtest = create_matrix(X_train, X_test, y_train, y_test).split(2)
predictions = train_model(param, num_round, dtrain, dtest)
```
Notice the stage we've created can take in both stage objects as well as standard inputs. After creating a stage, the useage is very similar to how normal functions are executed, making Foundations unintrusive to development practices.

##4. Validation and Results
Finally, lets validate our model! In the model.py file, we'll add a `best_results` function which will take in our model prediction matrix and return the indicies with the highest matches. Then, we will compare them against the output validation dataset and see how accurate our model is overall. We want to track the final accuracy of the model, which we will use `foundations.log_metric` to track. As more experiements are run, Foundations will record the different values of the accuracy, allowing you to compare models and identify what inputs were used to get the best result:

```python
"""
model.py
"""
def best_results(predictions, y_test):
	best_results = np.asarray([np.argmax(line) for line in predictions])
	precision = precision_score(y_test, best_results, average='macro')
	foundations.log_metric('Accuracy', precision)
```
In the driver.py file, we will use the previously created stage objects as inputs to the `best_results()` stage.

```python
"""
driver.py
"""
import foundations
from model import load_data, create_matrix, train_model, best_results

foundations.set_project_name("Xgboost Example")

load_data = foundations.create_stage(load_data)
create_matrix = foundations.create_stage(create_matrix)
train_model = foundations.create_stage(train_model)
best_results = foundations.create_stage(best_results)

param = {
    'max_depth': 1,  # the maximum depth of each tree
    'eta': 0.3,  # the training step for each iteration
    'silent': 1,  # logging mode - quiet
    'objective': 'multi:softprob',  # error evaluation for multiclass training
    'num_class': 3}  # the number of classes that exist in this datset
num_round = 1  # the number of training iterations

X_train, X_test, y_train, y_test = load_data().split(4)

dtrain, dtest = create_matrix(X_train, X_test, y_train, y_test).split(2)
predictions = train_model(param, num_round, dtrain, dtest)
results = best_results(predictions, y_test)
results.run()
```
Notice that we also call `.run()` on the final stage. When stages are created, Foundations tracks them with a directed acyclic graph (DAG) of the different defined stages. This allows stages to be run independently of each other for debugging or testing. In addition, all input and output stages prior to the executed stage in the DAG are automatically run as well so that the expected result can be properly captured.

Since we want to run the whole model workflow, we call `.run()` to the **last** stage in the pipeline. This signals to Foundations that essentially we want to run the final stage, as well as every previous stage which has inputs to the final one.

When we call `.run()` on the final stage, Foundations will execute all stages and properly pass in the returned values into the proper coressponding stages. Essentially, a graph of defined stages is created and will run all stages that lead to the final stage. This creates a workflow where each stage can have its own logging and tracking:
```
Foundations ─── load_data ──── create_matrix ──── train_model ──── best_results.run()
```
##5. Deploying the Model and Reading Results
Now we're ready to deploy the model! To run the model locally, we will use the Foundations CLI command `deploy`. In the project root directory run:
```bash
$ foundations deploy project_code/driver.py --env=local
```
If sucessfully deployed, Foundations will run the job on your local machine. To get the results of the model you can directly view it on the GUI if you have set it up locally, or through the SDK directly with the `get_metrics_for_all_jobs` [function](../reading_job_metrics/). 
```python
import foundations

print(foundations.get_metrics_for_all_jobs("XgBoost Example"))
"""
Returns a dataframe of all results
               completed_time                                job_id     project_name                  start_time     status     user  Accuracy
0  2019-03-18T14:08:30.207647  16c5459d-8afc-467c-83be-d5316957746b  XgBoost Example  2019-03-18T14:08:29.836108  completed  default  0.972222
"""
```
From our results, our model achieved a 97.22% accuracy! Try to see if you can improve these results by tuning the different parameters which can all be tracked with Foundations.

---
##Complete Model and Driver Files

**driver.py**
```python
import foundations
from model import load_data, create_matrix, train_model, best_results

foundations.set_project_name("Xgboost Example")

load_data = foundations.create_stage(load_data)
create_matrix = foundations.create_stage(create_matrix)
train_model = foundations.create_stage(train_model)
best_results = foundations.create_stage(best_results)

param = {
    'max_depth': 1,  # the maximum depth of each tree
    'eta': 0.3,  # the training step for each iteration
    'silent': 1,  # logging mode - quiet
    'objective': 'multi:softprob',  # error evaluation for multiclass training
    'num_class': 3}  # the number of classes that exist in this datset
num_round = 1  # the number of training iterations

X_train, X_test, y_train, y_test = load_data().split(4)

dtrain, dtest = create_matrix(X_train, X_test, y_train, y_test).split(2)
predictions = train_model(param, num_round, dtrain, dtest)
results = best_results(predictions, y_test)
results.run()
```
**model.py**
```python
"""
Each function here can be considered as a step (stage) towards building a model. Instead of having the whole model do everything in one script,
we break each step into individual functions, so that Foundations can create stages and keep track of each step
"""
import foundations
import numpy as np
import xgboost as xgb
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score

def load_data():
	iris = datasets.load_iris()
	X = iris.data
	y = iris.target
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

	return X_train, X_test, y_train, y_test

def create_matrix(X_train, X_test, y_train, y_test):
	dtrain = xgb.DMatrix(X_train, label=y_train)
	dtest = xgb.DMatrix(X_test, label=y_test)

	return dtrain, dtest

def train_model(param, iterations, training_data, test_data):
	boost = xgb.train(param, training_data, iterations)
	predictions = boost.predict(test_data)

	return predictions

def best_results(predictions, y_test):
	best_results = np.asarray([np.argmax(line) for line in predictions])
	precision = precision_score(y_test, best_results, average='macro')
	foundations.log_metric('Accuracy', precision)
```
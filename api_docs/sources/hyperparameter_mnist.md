<h1>Hyperparameter Tuning on the MNIST Dataset</h1>

**Note:** Is it highly recommended to look at the [MLP Neural Network](../mnist_example/) example before following this example.

In a previous [example](../mnist_example/), we looked at how to use Foundations to build and deploy a MLP neural net model. Now, we'll explore hyperparameter tuning with Foundations. When experimenting with various parameters, you will only need to deploy the job *once*, and Foundations will automatically take care of trying different models with different parameters, as well as tracking the results in a centralized place. We'll also be using [caching](../running_stages/#enable_caching) to help signifigantly reduce model training time.

You will need the files from the mnist [example](../mnist_example/), as we will be modifying the driver and model files. It's also recommended to create a new project with the Foundations CLI [command](../project_creation/#project-creation). The directory structure should look like this to run the model correctly:
```
mnist_hyperparameter_example
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
---
##Using Hyperparameters

Typically in model training, you'll have parameters that you'll want to vary across jobs while keeping the basic structure of the model itself the same (e.g. learning rate, number of neurons, etc.). By using a Hyperparameter object instead of an actual value, this creates a placeholder for Foundations to fill during the invocation of `.run()`. Foundations allows supplying arguments to the `.run()` function such as:  
```python
stage.run(A=0.25, B=100)
```
You can also pass in the different Hyperparameter values using both *params_dict* or keyword argument syntax as above. For more information on Hyperparameters and the `.run()` function, check out the documentation [here](../running_stages/#run)

In the previous MNIST example, we defined a few hyperparameters:
```python
#Define Hyperparameters for training different models
batch_size = 128
epoch = 5
```

Now, instead of manually altering the values each time and re-deploying indivudal jobs, we will use Foundations' Hyperparameter object to dynamically change the values during runtime, and track the different values as well as results. In addition, lets try experimenting around with the dropout rate defined in our model function. So first, lets convert those variables to Hyperparameters and create a new one:

```python
#Define Hyperparameters for training different models
batch_size = foundations.Hyperparameter('batch_size')
epoch = foundations.Hyperparameter('epoch')
drop_rate = foundations.Hyperparameter('drop_rate')
```

In our `build_model` function in the model.py file, we will need to now pass in the dropout rate as a variable:
```python
def build_model(dropout):
    model = Sequential()
    model.add(Dense(512, input_shape=(784,)))
    model.add(Activation('relu'))
    model.add(Dropout(dropout))
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(dropout))
    model.add(Dense(10))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model
```
Now, to pass in different values to our pipeline, we will create nested for-loops with different testable values so we can experiment with the different hyperparameters and see which combinations provide us with the best accuracy. Then, we associate those values with the hyperparameters by passing them into the `.run()` function. Foundations will dynamically use the values in each loop iteration when they are needed as well as track the values:

```python
for dropout_rate in [0.2, 0.5]:
    for batch_size in [128, 1024]:
        for epoch in [5, 10]:
            validation.run(dropout_rate=dropout_rate, batch_size=batch_size, epoch=epoch)
```

##Enabling Caching

Since Hyperparameter tuning leads to multiple jobs being run, it can often take up signifigant time and resources to run the whole pipeline multiple times. In order to make jobs more efficent, Foundations supports caching stages, which is useful when running multiple experiments where the input parameters don't change. 

In order to [enable caching](../running_stages/#enable_caching), we will call `.enable_caching()` at the end of our stage objects. Since loading the data and processing it will never change between different iterations, we'll enable caching on those stages:

```python
"""
driver.py
"""
# 1. Load data
X_train, X_test, y_train, y_test = load_data().enable_caching().split(4)

# 2. Process data
X_train, X_test, Y_train, Y_test = preprocess_data(
    X_train, X_test, y_train, y_test, num_classes).enable_caching().split(4)
```

Overall, our files now look like this:  
```python
"""
driver.py
"""
import foundations
from model import load_data, preprocess_data, build_model, train_model, eval_model

foundations.set_project_name("MNIST Hyperparameter Example")

# Create stages based off pipeline functions for Foundations to run
load_data = foundations.create_stage(load_data)
preprocess_data = foundations.create_stage(preprocess_data)
build_model = foundations.create_stage(build_model)
train_model = foundations.create_stage(train_model)
eval_model = foundations.create_stage(eval_model)

#Define Hyperparameters for training different models
num_classes = 10
batch_size = foundations.Hyperparameter('batch_size')
epoch = foundations.Hyperparameter('epoch')
dropout_rate = foundations.Hyperparameter('dropout_rate')

# 1. Load data
X_train, X_test, y_train, y_test = load_data().enable_caching().split(4)

# 2. Process data
X_train, X_test, Y_train, Y_test = preprocess_data(
    X_train, X_test, y_train, y_test, num_classes).enable_caching().split(4)

# 3. Build the neural net 
model = build_model(dropout_rate)

# 4.a Train the model
trained_model = train_model(batch_size, epoch, model, X_train, X_test, Y_train, Y_test)

# 4.b Validate the model
validation = eval_model(trained_model, X_test, Y_test)

#For each iteration, Foundations will deploy a new job and pass those values in as hyperparameters to the job
for dropout_rate in [0.2, 0.5]:
    for batch_size in [128, 1024]:
        for epoch in [5, 10]:
            validation.run(dropout_rate=dropout_rate, batch_size=batch_size, epoch=epoch)
```
```python
"""
model.py
"""
"""
Each function here can be considered as a step (stage) towards building a model. Instead of having the whole model do everything in one script,
we break each step into individual functions, so that Foundations can create stages and keep track of each step
"""

import numpy as np
import foundations

from keras.datasets import mnist
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.utils import np_utils

def load_data():
    (X_train, y_train), (X_test, y_test) = mnist.load_data()
    return X_train, X_test, y_train, y_test

def preprocess_data(X_train, X_test, y_train, y_test, num_classes):
    X_train = X_train.reshape(60000, 784)
    X_test = X_test.reshape(10000, 784)
    X_train = X_train.astype('float32')
    X_test = X_test.astype('float32')
    X_train /= 255
    X_test /= 255
    Y_train = np_utils.to_categorical(y_train, num_classes)
    Y_test = np_utils.to_categorical(y_test, num_classes)
    return X_train, X_test, Y_train, Y_test

def build_model(dropout):
    model = Sequential()
    model.add(Dense(512, input_shape=(784,)))
    model.add(Activation('relu'))
    model.add(Dropout(dropout))
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(dropout))
    model.add(Dense(10))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

def train_model(batch_size, epoch, model, X_train, X_test, Y_train, Y_test):
    result = model.fit(X_train, Y_train,
              batch_size=batch_size, nb_epoch=epoch, verbose=1,
              validation_data=(X_test, Y_test))
    return model

def eval_model(model, X_test, Y_test):
    score = model.evaluate(X_test, Y_test, verbose=1)
    foundations.log_metric('Test score:', score[0])
    foundations.log_metric('Test accuracy:', score[1])
```
Now, lets run the model! Using the [deploy] (../project_creation/#deploying-jobs) command and deploying the driver.py file will result in 8 total jobs being run. When fetching results, you should expect a dataframe similar to the following:

```python
import foundations
print(foundations.get_metrics_for_all_jobs("MNIST Hyperparameter Example"))
"""
               completed_time                                job_id                  project_name                  start_time     status     user  batch_size  dropout_rate  epoch  Test accuracy:  Test score:
0  2019-03-18T17:14:16.615247  880c73da-ac07-4be3-8355-6df63e836375  MNIST Hyperparameter Example  2019-03-18T17:13:58.720507  completed  default        1024           0.5      5          0.9700     0.091344
1  2019-03-18T17:15:04.161472  74962d23-f44a-496b-8ae9-2699098dd5bf  MNIST Hyperparameter Example  2019-03-18T17:14:29.519180  completed  default        1024           0.5     10          0.9805     0.063361
2  2019-03-18T17:09:21.244396  5704d968-53cd-4f75-9b83-28945b96f389  MNIST Hyperparameter Example  2019-03-18T17:08:54.237384  completed  default         128           0.2      5          0.9783     0.070758
3  2019-03-18T17:12:36.409258  45993805-290e-4a88-9c2b-3112ebc17cae  MNIST Hyperparameter Example  2019-03-18T17:12:08.739026  completed  default         128           0.5      5          0.9775     0.068682
4  2019-03-18T17:11:53.960767  e2f021f1-d30a-4303-8f43-ff44965c7be1  MNIST Hyperparameter Example  2019-03-18T17:11:17.755423  completed  default        1024           0.2     10          0.9809     0.060631
5  2019-03-18T17:10:30.462125  66d4e6d4-6ebd-4c14-bbff-3d8ef32e77e6  MNIST Hyperparameter Example  2019-03-18T17:09:35.938155  completed  default         128           0.2     10          0.9837     0.062238
6  2019-03-18T17:13:44.496215  70a097e5-fc35-4ba9-9856-3b485de40d01  MNIST Hyperparameter Example  2019-03-18T17:12:50.514814  completed  default         128           0.5     10          0.9819     0.059160
7  2019-03-18T17:11:03.505060  a628ac4c-ad92-4f3c-8f9f-3518ca57aad2  MNIST Hyperparameter Example  2019-03-18T17:10:44.915265  completed  default        1024           0.2      5          0.9757     0.073972
"""
```

In the dataframe above, you can see the different Hyperparameters we passed into the final stage during runtime as well as the final accuracy scores, making it easy to see the different experiments and compare results.

##Advanced Hyperparameter Features

In the example above, we demomstrated how to use Hyperparameters to fine-tune a model. However, when we ran the Hyperparameters, we used a bunch of nested-for loops to pass in values. This sounds like annoying boilerplate, and it is! So now, we'll explore some advance features that make Hyperparameter tuning cleaner.

First, we'll introduce the DiscreteHyperparameter object, which represents a discrete iterable of values a hyperparameter may
take. It's essentially a list with an interface better tuned toward hyperparameter search/tuning. Now, instead of writing nested for-loops, we can replace them with:

```python
"""
driver.py
"""
#For each iteration, Foundations will deploy a new job and pass those values in as hyperparameters to the job
params_ranges = {
    'dropout_rate': foundations.DiscreteHyperparameter([0.2, 0.5]),
    'batch_size': foundations.DiscreteHyperparameter([128, 1024]),
    'epoch': foundations.DiscreteHyperparameter([5, 10])
}
    validation.run(dropout_rate=dropout_rate, batch_size=batch_size, epoch=epoch)
```

Each stage still requires us to pass in the standard foundations.Hyperparameter objects to define them within each stage so that Foundations knows what variables are dynamically generated during runtime, but when we are executing the pipeline we can use the DiscreteHyperparameter object as a more efficent interface to signal iterable values.

Next, to pass in the `params_ranges` dictionary, we'll be using the `.grid_search()` function on the validation stage which essentially replaces the `.run()` command. `.grid_search()` basically automates the nested loops so that all you need to do is supply ranges the hyperparameters may take:
```python
"""
driver.py
"""
params_ranges = {
    'dropout_rate': foundations.DiscreteHyperparameter([0.2, 0.5]),
    'batch_size': foundations.DiscreteHyperparameter([128, 1024]),
    'epoch': foundations.DiscreteHyperparameter([5, 10])
}
# the below line of code is equivalent to:
#
# for dropout_rate in [0.2, 0.5]:
#   for batch_size in [128, 1024]:
#       for epoch in [5, 10]:
#           validation.run(validation.run(dropout_rate=dropout_rate, batch_size=batch_size, epoch=epoch))
#
# Foundations automates this boilerplate away with the .grid_search() method
validation.grid_search(params_ranges)
```
The new driver.py file should now look like:
```python
"""
driver.py
"""
import foundations
from model import load_data, preprocess_data, build_model, train_model, eval_model

foundations.set_project_name("MNIST Hyperparameter Example")

# Create stages based off pipeline functions for Foundations to run
load_data = foundations.create_stage(load_data)
preprocess_data = foundations.create_stage(preprocess_data)
build_model = foundations.create_stage(build_model)
train_model = foundations.create_stage(train_model)
eval_model = foundations.create_stage(eval_model)

#Define Hyperparameters for training different models
num_classes = 10
batch_size = foundations.Hyperparameter('batch_size')
epoch = foundations.Hyperparameter('epoch')
dropout_rate = foundations.Hyperparameter('dropout_rate')

# 1. Load data
X_train, X_test, y_train, y_test = load_data().enable_caching().split(4)

# 2. Process data
X_train, X_test, Y_train, Y_test = preprocess_data(
    X_train, X_test, y_train, y_test, num_classes).enable_caching().split(4)

# 3. Build the neural net 
model = build_model(dropout_rate)

# 4.a Train the model
trained_model = train_model(batch_size, epoch, model, X_train, X_test, Y_train, Y_test)

# 4.b Validate the model
validation = eval_model(trained_model, X_test, Y_test)

params_ranges = {
    'dropout_rate': foundations.DiscreteHyperparameter([0.2, 0.5]),
    'batch_size': foundations.DiscreteHyperparameter([128, 1024]),
    'epoch': foundations.DiscreteHyperparameter([5, 10])
}
# the below line of code is equivalent to:
#
# for dropout_rate in [0.2, 0.5]:
#   for batch_size in [128, 1024]:
#       for epoch in [5, 10]:
#           validation.run(validation.run(dropout_rate=dropout_rate, batch_size=batch_size, epoch=epoch))
#
# Foundations automates this boilerplate away with the .grid_search() method
validation.grid_search(params_ranges)
```
Deploying the code above should produce the same output as running the Hyperparameter search with for-loops. 

---
##Complete Model and Driver Files

**driver.py**
```python
"""
driver.py
"""
import foundations
from model import load_data, preprocess_data, build_model, train_model, eval_model

foundations.set_project_name("MNIST Hyperparameter Example")

# Create stages based off pipeline functions for Foundations to run
load_data = foundations.create_stage(load_data)
preprocess_data = foundations.create_stage(preprocess_data)
build_model = foundations.create_stage(build_model)
train_model = foundations.create_stage(train_model)
eval_model = foundations.create_stage(eval_model)

#Define Hyperparameters for training different models
num_classes = 10
batch_size = foundations.Hyperparameter('batch_size')
epoch = foundations.Hyperparameter('epoch')
dropout_rate = foundations.Hyperparameter('dropout_rate')

# 1. Load data
X_train, X_test, y_train, y_test = load_data().enable_caching().split(4)

# 2. Process data
X_train, X_test, Y_train, Y_test = preprocess_data(
    X_train, X_test, y_train, y_test, num_classes).enable_caching().split(4)

# 3. Build the neural net 
model = build_model(dropout_rate)

# 4.a Train the model
trained_model = train_model(batch_size, epoch, model, X_train, X_test, Y_train, Y_test)

# 4.b Validate the model
validation = eval_model(trained_model, X_test, Y_test)

params_ranges = {
    'dropout_rate': foundations.DiscreteHyperparameter([0.2, 0.5]),
    'batch_size': foundations.DiscreteHyperparameter([128, 1024]),
    'epoch': foundations.DiscreteHyperparameter([5, 10])
}

validation.grid_search(params_ranges)
```
**model.py**
```python
"""
model.py
"""
"""
Each function here can be considered as a step (stage) towards building a model. Instead of having the whole model do everything in one script,
we break each step into individual functions, so that Foundations can create stages and keep track of each step
"""

import numpy as np
import foundations

from keras.datasets import mnist
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.utils import np_utils

def load_data():
    (X_train, y_train), (X_test, y_test) = mnist.load_data()
    return X_train, X_test, y_train, y_test

def preprocess_data(X_train, X_test, y_train, y_test, num_classes):
    X_train = X_train.reshape(60000, 784)
    X_test = X_test.reshape(10000, 784)
    X_train = X_train.astype('float32')
    X_test = X_test.astype('float32')
    X_train /= 255
    X_test /= 255
    Y_train = np_utils.to_categorical(y_train, num_classes)
    Y_test = np_utils.to_categorical(y_test, num_classes)
    return X_train, X_test, Y_train, Y_test

def build_model(dropout):
    model = Sequential()
    model.add(Dense(512, input_shape=(784,)))
    model.add(Activation('relu'))
    model.add(Dropout(dropout))
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(dropout))
    model.add(Dense(10))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

def train_model(batch_size, epoch, model, X_train, X_test, Y_train, Y_test):
    result = model.fit(X_train, Y_train,
              batch_size=batch_size, nb_epoch=epoch, verbose=1,
              validation_data=(X_test, Y_test))
    return model

def eval_model(model, X_test, Y_test):
    score = model.evaluate(X_test, Y_test, verbose=1)
    foundations.log_metric('Test score:', score[0])
    foundations.log_metric('Test accuracy:', score[1])
```
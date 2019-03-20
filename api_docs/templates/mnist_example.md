<h1>Training a Neural Network on the MNIST Dataset</h1>

In this example, we will use Foundations and Keras to train a simple Neural Net on the famous MNIST dataset. We will be leveraging the dataset directly from keras, so no download of data is required. It is highly recommended to first create a new project using the Foundations CLI [command](../project_creation/#project-creation). The following example code will then go directly into the driver.py and model.py files respectively.

The workflow of the example will be as follows:  
<span>1. </span> Load the data  
<span>2. </span> Prepare the data  
<span>3. </span> Build the neural net  
<span>4. </span> Model training and validation

Rather than run the whole model in one call, we divide each step in the model into a stage, so that Foundations can wrap the your code in layers which perform provenance tracking, caching, prepping your job for deployment, etc.

Some additional python dependencies you may need to install include: `keras` `tensorflow`

The directory structure should look like this to run the model correctly:
```
mnist_example
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

Note: This is **not** a complete course on deep learning. Instead, this tutorial is meant to get you from zero to your first 
model trained with Foundations with as little headache as possible!
---
##1. Load the dataset
First, lets load the dataset we'll be using for this example in the model.py file. Since we'll be using Keras, we'll need to import the dataset as well as a few other dependencies. 

```python
"""
model.py
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
```

In the driver.py file, we can now create our first stage (or step in the pipeline) for Foundations to manage.

```python
"""
driver.py
"""
import foundations

from model import load_data

# Set a project a name so that Foundations knows how to track the model when it is deployed
foundations.set_project_name("MNIST Example")

load_data = foundations.create_stage(load_data)

X_train, X_test, y_train, y_test = load_data().split(4)
```
Here, we've turned the `load_data` function into a Foundations stage which returns a callable with the exact same signature as the input `load_data` function. When Foundations runs the pipeline, it will be called in the same way as the input function, but will return a stage object instead which Foundations uses to track inputs and outputs.

Also, notice how we split the dataset above into training and test data. Because of this, when we turn `load_data` into a stage for Foundations to manage, we'll need to use the `.split()` [function](../running_stages/#split) in the driver file so that we correctly capture the number of returned values.  

##2. Prepare the data
Now that we have the data available, we need preprocess the data to ensure that our model can properly handle it. For example,  we will need to reduce the images down into a vector of pixels so that our MLP model can properly understand the inputs. We also want to normalize the pixel values from grey-scale to values between 0 and 1, as well as encode the outputs to values between 0-9 so we can classify the values in the images. In the model.py lets add a new function:

```python
"""
model.py
"""
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
```
In the driver.py, we can create a stage out of the preprocess_data function:  

```python
"""
driver.py
"""
import foundations

from model import load_data, preprocess_data

foundations.set_project_name("MNIST Example")

load_data = foundations.create_stage(load_data)
preprocess_data = foundations.create_stage(preprocess_data)

X_train, X_test, y_train, y_test = load_data().split(4)

X_train, X_test, Y_train, Y_test = preprocess_data(X_train, X_test, y_train, y_test, 10).split(4)
```
Here we pipe the outputs of the `load_data()` stage into the `preprocess_data()` stage. Outputs of one stage can be treated as standard variables, and can be used in future stages. Because the `preprocess_data` input function returns 4 values, we need to use `.split()` again to indicate to Foundations how many values are generated from the input function.

##3. Build the model
Now that we have loaded and processed the data, the next step is to build out our neural net using keras. Let's add a `build_model` function in the model.py file:  
```python
"""
model.py
"""
def build_model():
    model = Sequential()
    model.add(Dense(512, input_shape=(784,)))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))
    model.add(Dense(10))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    return model
```
In the driver.py file we create a `build_model` stage as the next step in our pipeline after loading and processing the data:
```python
"""
driver.py
"""
import foundations

from model import load_data, preprocess_data, build_model

foundations.set_project_name("MNIST Example")

load_data = foundations.create_stage(load_data)
preprocess_data = foundations.create_stage(preprocess_data)
build_model = foundations.create_stage(build_model)

X_train, X_test, y_train, y_test = load_data().split(4)

X_train, X_test, Y_train, Y_test = preprocess_data(X_train, X_test, y_train, y_test, 10).split(4)

model = build_model()
```
Although the stage we've created doesn't take in any inputs relative to previous stages in the pipeline, Foundations will still return a stage object which can be used in other future stages.

##4. Model Training and Validation
Finally, lets train our model! In the model.py file, lets add two functions: one for fitting the model itself, and one for evaluating the output results. Both functions require a keras model object as an input, which we will pass in through the driver.py file when we add these steps to the Foundations pipeline. We also want to track the final score and accuracy of the model, which we will use `foundations.log_metric` to track. As more experiements are run, Foundations will record the different values of the accuracy, allowing you to compare models and identify what inputs were used to get the best result:

```python
"""
model.py
"""
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
In the driver.py file, we will use the previously created stage objects as inputs to the `train_model()` and `eval_model()` stages. After creating a stage, the useage is very similar to how normal functions are executed, making Foundations unintrusive to development practices.  

```python
"""
driver.py
"""
import foundations

from model import load_data, preprocess_data, build_model, train_model, eval_model

foundations.set_project_name("MNIST Example")

# Create stages based off pipeline functions for Foundations to run
load_data = foundations.create_stage(load_data)
preprocess_data = foundations.create_stage(preprocess_data)
build_model = foundations.create_stage(build_model)
train_model = foundations.create_stage(train_model)
eval_model = foundations.create_stage(eval_model)

# 1. Load data
X_train, X_test, y_train, y_test = load_data().split(4)

# 2. Process data
X_train, X_test, Y_train, Y_test = preprocess_data(X_train, X_test, y_train, y_test, 10).split(4)

# 3. Build the neural net 
model = build_model()

# 4.a Train the model
trained_model = train_model(128, 5, model, X_train, X_test, Y_train, Y_test)

# 4.b Validate the model
validation = eval_model(trained_model, X_test, Y_test)
```
Now that we've created five stages, the last thing is to let Foundations which one to execute. Since we want to run the whole pipeline, we call `.run()` to the **last** stage in the pipeline. This signals to Foundations that essentially we want to run the final stage, as well as every previous stage which has inputs to the final one.

```python
validation.run()
```
When we call `.run()` on the final stage, Foundations will execute all stages and properly pass in the returned values into the proper coressponding stages. Essentially, a graph of defined stages is created and will run all stages that lead to the final stage. This creates a workflow where each stage can have its own logging and tracking:
```
Foundations ─── load_data ──── preprocess_data ──── train_model ──── validation.run()
             │                                   │
             └─────────── build_model ───────────┘
```
##5. Deploying the Model and Reading Results
Now we're ready to deploy the model! To run the model locally, we will use the Foundations CLI command `deploy`. In the project root directory run:
```bash
$ foundations deploy project_code/driver.py --env=local
```
If sucessfully deployed, Foundations will run the job on your local machine. You can see from the output that the model ran 5 iterations with a batch size of 1028 samples, giving us a final accuracy of 97.88%!
```
Train on 60000 samples, validate on 10000 samples
Epoch 1/5
2019-03-18 13:03:41.023255: I tensorflow/core/platform/cpu_feature_guard.cc:141] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2 FMA
60000/60000 [==============================] - 6s 92us/step - loss: 0.2520 - acc: 0.9244 - val_loss: 0.1162 - val_acc: 0.9639
Epoch 2/5
60000/60000 [==============================] - 5s 90us/step - loss: 0.0998 - acc: 0.9688 - val_loss: 0.0836 - val_acc: 0.9735
Epoch 3/5
60000/60000 [==============================] - 12s 208us/step - loss: 0.0730 - acc: 0.9773 - val_loss: 0.0777 - val_acc: 0.9757
Epoch 4/5
60000/60000 [==============================] - 9s 153us/step - loss: 0.0570 - acc: 0.9819 - val_loss: 0.0729 - val_acc: 0.9781
Epoch 5/5
60000/60000 [==============================] - 7s 110us/step - loss: 0.0457 - acc: 0.9851 - val_loss: 0.0653 - val_acc: 0.9788
2019-03-18 13:04:20,265 - foundations_contrib.middleware.stage_logging_middleware - INFO - Finished stage train_model (uuid: 2e93c5f81d7b66c87d8b7993fe1ebce0ef7e077b)
2019-03-18 13:04:20,273 - foundations_contrib.middleware.stage_logging_middleware - INFO - Running stage `eval_model` (uuid: `48bc3177feacc0b6fa67d730651aa6165b495ffb`), file: /Users/ericliou/Documents/TestInstalling/mnist_example/project_code/a6c1722f-6b08-4266-9290-ad24b5128455/model.py, line: 51
10000/10000 [==============================] - 1s 57us/step
Test score: 0.06534448580869356
Test accuracy: 0.9788
```
To view the results, you can directly view it on the GUI if you have set it up locally, or through the SDK directly with the `get_metrics_for_all_jobs` [function](../reading_job_metrics/). 
```python
import foundations

print(foundations.get_metrics_for_all_jobs("MNIST Example"))
"""
Returns a dataframe of all results
               completed_time                                job_id   project_name     ...         user  Test accuracy: Test score:
0  2019-03-13T15:06:31.554495  6b94b13f-7beb-4d6d-9a55-c81a203807ea  MNIST Example     ...      default            NaN         NaN
1  2019-03-14T14:36:40.643822  f5ba0d2b-0e5b-4711-b6be-268d8773618e  MNIST Example     ...      default         0.9799    0.063373
2  2019-03-13T15:11:37.867263  6964dd5c-a8f4-467a-8c45-2acbe04bc0c4  MNIST Example     ...      default         0.9801    0.066460
3  2019-03-13T15:09:04.754330  dc82e2e7-4e2a-4461-aca5-2164b923843e  MNIST Example     ...      default         0.9807    0.067655
4  2019-03-13T15:07:54.400889  5e0def81-d797-4bd5-8054-94fea04bcb44  MNIST Example     ...      default         0.9808    0.062498
5  2019-03-13T14:54:20.103170  94b05371-f748-4b53-9723-6e1c7be8e767  MNIST Example     ...      default            NaN         NaN
6  2019-03-18T13:04:20.902782  a6c1722f-6b08-4266-9290-ad24b5128455  MNIST Example     ...      default         0.9788    0.065344
7  2019-03-14T14:27:04.355402  ad39d597-1d85-46de-87ad-5b9cf1d62167  MNIST Example     ...      default         0.9796    0.071707
8  2019-03-13T15:04:47.593663  4bb3a193-ddc1-4103-81e9-85ef903c8978  MNIST Example     ...      default            NaN         NaN
9  2019-03-13T15:00:48.441150  d1b8569b-90d3-4638-bff7-c2b9538ea292  MNIST Example     ...      default            NaN         NaN
"""
```

To further improve the model, you can experiment with different models, transformations, and hyperparameters which can all be tracked with Foundations.

---
##Complete Model and Driver Files

**driver.py**
```python
import foundations

from model import load_data, preprocess_data, build_model, train_model, eval_model

foundations.set_project_name("MNIST Example")

# Create stages based off pipeline functions for Foundations to run
load_data = foundations.create_stage(load_data)
preprocess_data = foundations.create_stage(preprocess_data)
build_model = foundations.create_stage(build_model)
train_model = foundations.create_stage(train_model)
eval_model = foundations.create_stage(eval_model)

#Define Hyperparameters for training different models
num_classes = 10
batch_size = 128
epoch = 5

# 1. Load data
X_train, X_test, y_train, y_test = load_data().split(4)

# 2. Process data
X_train, X_test, Y_train, Y_test = preprocess_data(X_train, X_test, y_train, y_test, num_classes).split(4)

# 3. Build the neural net 
model = build_model()

# 4.a Train the model
trained_model = train_model(batch_size, epoch, model, X_train, X_test, Y_train, Y_test)

# 4.b Validate the model
validation = eval_model(trained_model, X_test, Y_test)

validation.run()
```
**model.py**
```python
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

def build_model():
    model = Sequential()
    model.add(Dense(512, input_shape=(784,)))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dropout(0.2))
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
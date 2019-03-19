<h1>Training a Logistic Regression Model on the Titanic Dataset</h1>

In this example, we will demonstrate how Foundations can be used create a pipeline when training a logistic regression model on a well-known Kaggle dataset: [Titanic: Machine Learning from Disaster](https://www.kaggle.com/c/titanic).

The workflow of the example will be as follows:  
<span>1. </span> Load the data  
<span>2. </span> Prepare the data  
<span>3. </span> Basic transformations and feature engineering  
<span>4. </span> Model training and Validation  

It is recommended to first create a new project using the Foundations CLI [command](../project_creation/#project-creation). Then, download the `train.csv` from the Kaggle link above, rename it to `titanic.csv`, and place it in the `data` directory. In this example, we will splitting the dataset up into both training and validation sets from this one CSV. 

Some additional python dependencies you may need to install include: `pandas`  `PyYaml`  `sklearn`  `scipy`
 
This example will also use utility code commonly used during data preparation/data cleaning, as well as extracting, transforming, and loading the data into models. In the Foundations framework, code is expected to be structured into stages - instead of a monolithic code block, you have functions which represent stages in a job. 

In order to run this example, it is highly recommended to create a new `utilities` directory in the project_code folder and add the utility files below. The directory structure should look like this to run the model correctly:
```
titanic
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
For additional information on how to deploy the model, check out our documentation [here](../configs/#how-to-deploy)

Note: This is **not** a complete course on deep learning. Instead, this tutorial is meant to demonstrate a more complex model which you can train with Foundations with as little headache as possible!

---
##Model and Driver Files

The following files are where the Foundations pipeline will be created and deployed, as well as the model code itself. Since we'll be using a logistic regression model from the sklearn library, there won't be a lot of code in the model file itself. Check out our other examples for different model examples.

**driver.py**
```python
import foundations
from model import train_logistic_regression
from utilities.prep import union
from utilities.logging import log_formatted
from utilities.data_pipeline import load_data, fill_categorical_nulls, split_inputs_and_targets, 
    split_training_and_validation, impute, one_hot_encode, drop_non_numeric_columns, get_metrics

# Create stages based off pipeline functions for Foundations to run
union = foundations.create_stage(union)
train_logistic_regression = foundations.create_stage(train_logistic_regression)
log_formatted = foundations.create_stage(log_formatted)
load_data = foundations.create_stage(load_data)
fill_categorical_nulls = foundations.create_stage(fill_categorical_nulls)
split_inputs_and_targets = foundations.create_stage(split_inputs_and_targets)
split_training_and_validation = foundations.create_stage(split_training_and_validation)
impute = foundations.create_stage(impute)
one_hot_encode = foundations.create_stage(one_hot_encode)
drop_non_numeric_columns = foundations.create_stage(drop_non_numeric_columns)
get_metrics = foundations.create_stage(get_metrics)

# Set the project name
foundations.set_project_name('Titanic Logistic Example')

# 1. Load the data
data = load_data()

# 2. Prepare the data 
data = fill_categorical_nulls(data=data)
# Here we use .split since the function returns two parameters to explictly let Foundations know there are two return values
inputs, targets = split_inputs_and_targets(data=data).split(2)

# 3. Feature egineering and splitting dataset
x_train, x_valid, y_train, y_valid = split_training_and_validation(
    inputs=inputs, targets=targets).split(4)
x_train, x_valid = impute(x_train=x_train, x_valid=x_valid).split(2)
x_train, x_valid = one_hot_encode(x_train=x_train, x_valid=x_valid).split(2)
x_train, x_valid = drop_non_numeric_columns(x_train=x_train, x_valid=x_valid).split(2)

# 4. Model training and scoring
model = train_logistic_regression(x_train=x_train, y_train=y_train)
y_train, train_score = get_metrics(
    model=model, inputs=x_train, targets=y_train, data_set_name='Training').split(2)
    
# Validate model
y_valid, valid_score = get_metrics(
    model=model, inputs=x_valid, targets=y_valid, data_set_name='Validation').split(2)
results = union(first=y_train, second=y_valid)

# Print out the results
log_formatted('\nData: {}\nTraining score was {}\nValidation score was {}',
                results, train_score, valid_score).run()
```
**model.py**
```python
from sklearn.linear_model import LogisticRegression

def train_logistic_regression(x_train, y_train, *logistic_regression_args, **logistic_regression_kwargs):
    model = LogisticRegression(*logistic_regression_args, **logistic_regression_kwargs)
    model = model.fit(x_train, y_train)

    return model
```
---
##Utility Classes and Functions  

**encoder_wrapper.py**
```python
class EncoderWrapper(object):
    """
    A convenience class that wraps an arbitrary class which provides encoding functionality.
    """
    
    def __init__(self, encoder, columns):
        self._encoder = encoder
        self._columns = columns

    def fit(self, data_frame):
        self._encoder.fit(data_frame[self._columns])
        return self

    def transform(self, data_frame):
        from utils.prep import encode
        return encode(data_frame, self._encoder, self._columns)
```
**one_hot_encoder.py**
```python
class OneHotEncoder(object):
    """
    A utility class which can create a one-hot encoding as well as fit a dataframe
    to it later.
    """
    def __init__(self):
        self._allowed_values = {}

    def fit(self, data_frame):
        for column in data_frame:
            self._allowed_values[column] = data_frame[column].unique()
        return self

    def transform(self, data_frame):
        from common.prep import get_mode, impute_for_one_hot, one_hot_encode

        for column in data_frame:
            values = self._allowed_values[column]
            mode = get_mode(data_frame, column)
            data_frame = impute_for_one_hot(data_frame, column, values, mode)
            data_frame = one_hot_encode(data_frame, column)

            for value in values:
                encoded_column = '{}_{}'.format(column, value)
                if not encoded_column in data_frame:
                    data_frame[encoded_column] = 0

        return data_frame
```  
**prep.py**  
```python
import pandas as pd
from sklearn.preprocessing import Imputer
from utils.encoder_wrapper import EncoderWrapper
from utils.one_hot_encoder import OneHotEncoder

def fillna(data_frame, column, value):
    data_frame[column].fillna(value, inplace=True)
    return data_frame

def impute_for_one_hot(data_frame, column, allowed_values, value):
    data_frame.loc[~data_frame[column].isin(allowed_values), column] = value
    return data_frame

def one_hot_encode(data_frame, column):
    encoding = pd.get_dummies(data_frame[column], prefix=column)
    for new_column in encoding:
        assign_columns(data_frame, new_column, encoding[new_column])
    return data_frame

def get_mode(data_frame, column):
    data_frame_without_nans = data_frame.dropna(subset=[column])
    return data_frame_without_nans[column].value_counts().idxmax()

def encode(data_frame, encoder, columns):
    results = encoder.transform(data_frame[columns])
    if isinstance(results, pd.DataFrame):
        for column in results:
            assign_columns(data_frame, column, results[column])
    else:
        assign_columns(data_frame, columns, results)
    return data_frame

def assign_columns(data_frame, columns, value):
    data_frame[columns] = value
    return data_frame

def union(first, second):
    return pd.concat([first, second])

def require(data, *args):
    return data

def train_imputer(data_frame, numeric_columns, *imputer_args, **imputer_kwargs):

    encoder = Imputer(*imputer_args, **imputer_kwargs)
    encoder = EncoderWrapper(encoder, numeric_columns)
    encoder = encoder.fit(data_frame)

    return encoder

def train_one_hot_encoder(data_frame, categorical_columns):
    encoder = OneHotEncoder()
    encoder = EncoderWrapper(encoder, categorical_columns)
    encoder = encoder.fit(data_frame)

    return encoder

def drop_non_numeric(data_frame):
    return data_frame.select_dtypes(['number'])
```
**logging.py**
```python
def log_data(data):
    _log().info(repr(data))
    return data

def log_formatted(format_string, *args):
    _log().info(format_string.format(*args))
    return args

def _log():
    from foundations import log_manager
    return log_manager.get_logger(__name__)
```
**data_pipeline.py**
```python
from utils.prep import fillna, train_imputer, train_one_hot_encoder, drop_non_numeric
from sklearn.model_selection import train_test_split
import pandas as pd
import foundations

def load_data():
    return pd.read_csv('../../data/titanic.csv')

def fill_categorical_nulls(data):
    data = fillna(data, 'Cabin', 'NULLCABIN')
    data = fillna(data, 'Embarked', 'NULLEMBARKED')
    return data

def split_inputs_and_targets(data):
    inputs = data[['Age', 'SibSp', 'Parch', 'Fare',
                   'Pclass', 'Sex', 'Cabin', 'Embarked']]
    targets = data[['Survived']]
    return inputs, targets

def split_training_and_validation(inputs, targets):
    return train_test_split(inputs, targets, test_size=0.2, random_state=42, stratify=targets.as_matrix())

def create_imputer(data):
    return train_imputer(data, ['Age', 'Fare'])

def impute(x_train, x_valid):
    encoder = create_imputer(x_train)
    x_train = encoder.transform(x_train)
    x_valid = encoder.transform(x_valid)
    return x_train, x_valid

def create_one_hot_encoder(data):
    return train_one_hot_encoder(data, ['Pclass', 'Sex', 'Cabin', 'Embarked'])

def one_hot_encode(x_train, x_valid):
    encoder = create_one_hot_encoder(x_train)
    x_train = encoder.transform(x_train)
    x_valid = encoder.transform(x_valid)
    return x_train, x_valid

def drop_non_numeric_columns(x_train, x_valid):
    x_train = drop_non_numeric(x_train)
    x_valid = drop_non_numeric(x_valid)
    return x_train, x_valid

def get_metrics_internal(model, x_values, y_values):
    score = model.score(x_values, y_values)
    y_valid_predications = model.predict(x_values)
    return y_valid_predications, score

def get_metrics(model, inputs, targets, data_set_name):
    targets_predications, score = get_metrics_internal(
        model, inputs, targets)
    targets['PredictedSurvived'] = targets_predications
    targets['Type'] = 'Training'

    metric_prefix = str(data_set_name).lower()

    foundations.log_metric('{}_score'.format(metric_prefix), score)
    foundations.log_metric('data_set_name', data_set_name)

    return targets, score
```
---

"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""

import foundations
from foundations_production import preprocessor, Transformer, Model
import pandas

class AddAverageToValueTransformer(object):

    def __init__(self):
        self.average = 0

    def fit(self, data):
        selected_data = data[["Sex", "Cabin", "Fare"]]
        self.average = selected_data.mean()

    def transform(self, data):
        data[["Sex", "Cabin", "Fare"]] = data[["Sex", "Cabin", "Fare"]] + self.average
        return data

class TestModel(object):

    def __init__(self):
        self.max_fare = 0

    def fit(self, input_training_features, input_training_targets, input_validation_features, input_validation_targets):
        self.max_fare = input_training_features["Fare"].max()

    def predict(self, input_features):
        predicted_labels = []
        for row in input_features["Fare"]:
            predicted_labels.append(int(row < self.max_fare))
        return pandas.DataFrame({"Survived": predicted_labels})

@preprocessor
def preprocessor(input_data):
    transformer = Transformer(AddAverageToValueTransformer)
    transformer.fit(input_data)
    return transformer.transform(input_data)

def split_inputs_and_targets(data):
    if "Survived" in data:
        return data[["Sex", "Cabin", "Fare"]], data[["Survived"]]
    else:
        return data[["Sex", "Cabin", "Fare"]], None

def split_data(train_data, validation_data):
    split_inputs_and_targets_stage = foundations.create_stage(split_inputs_and_targets)
    train_features, train_targets = split_inputs_and_targets_stage(train_data).split(2)
    validation_features, validation_targets = split_inputs_and_targets_stage(validation_data).split(2)
    return train_features, train_targets, validation_features, validation_targets

train_data = pandas.DataFrame({
    "Sex": [0, 1, 4],
    "Cabin": [200, 100, 0],
    "Fare": [40, 20, -200],
    "Survived": [0, 1, 1]
})

validation_data = pandas.DataFrame({
    "Sex": [0],
    "Cabin": [101],
    "Fare": [10],
    "Survived": [1]
})

preprocessed_train_data = preprocessor(train_data)

preprocessor.set_inference_mode()
preprocessed_validation_data = preprocessor(validation_data)
train_features, train_targets, validation_features, validation_targets = split_data(preprocessed_train_data, preprocessed_validation_data)

model = Model(TestModel)
model.fit(train_features, train_targets, validation_features, validation_targets)
validation_predictions = model.predict(validation_features)

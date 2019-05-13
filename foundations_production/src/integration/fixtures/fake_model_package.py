"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Susan Davis <s.davis@dessa.com>, 04 2019
"""

from foundations_production import preprocessor, Transformer, Model
import pandas


class FakeModel(object):
    def fit(self, *args):
        pass

    def predict(self, data):
        data['1st column'] += ' predicted'
        data['2nd column'] += 100
        return data

class FakeTransformer(object):

    def __init__(self):
        self.num_to_add = 333

    def fit(self, data):
        pass

    def transform(self, data):
        data['1st column'] += ' transformed'
        data['2nd column'] += self.num_to_add
        return data


@preprocessor
def preprocessor(input_data):
    transformer = Transformer(FakeTransformer)
    transformer.fit(input_data)
    return transformer.transform(input_data)


train_data = pandas.DataFrame({
    '1st column': ['value', 'spider'],
    '2nd column': [43234, 323]
})

validation_data = train_data

preprocessed_train_data = preprocessor(train_data)

model = Model(FakeModel)
model.fit(preprocessed_train_data)
validation_predictions = model.predict(validation_data)

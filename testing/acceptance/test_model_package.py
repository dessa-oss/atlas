"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *
import pandas


class TestModelPackage(Spec):

    class AddAverageToValueTransformer(object):

        def __init__(self):
            self.average = 0

        def fit(self, data):
            self.average = data.mean()

        def transform(self, data):
            return data + self.average

    class Model(object):

        def __init__(self):
            self.max_fare = 0

        def fit(self, input_training_features, input_training_targets, input_validation_features, input_validation_targets):
            self.max_fare = input_training_features["Fare"].max()

        def predict(self, input_features):
            predicted_labels = []
            for row in input_features["Fare"]:
                predicted_labels.append(int(row < self.max_fare))
            return pandas.DataFrame({"Survived": predicted_labels})
    
    @skip('Not ready yet')
    def test_can_create_and_consume_model_package(self):
        import foundations.production

        foundations.set_project_name('production_titanic_test')

        @foundations.production.preprocessor
        def preprocessor(input_data):
            transformer = foundations.production.Transformer(["Sex", "Cabin", "Fare"], self.AddAverageToValueTransformer)
            transformer.fit(input_data)
            return transformer.transform(input_data)

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

        @foundations.production.model
        def model(train_data, validation_data):
            train_features = train_data[["Sex", "Cabin", "Fare"]]
            train_targets = train_data[["Survived"]]
            validation_features = validation_data[["Sex", "Cabin", "Fare"]]
            validation_targets = validation_data[["Survived"]]

            model_transformer = foundations.production.Model(self.Model)
            model_transformer.fit(train_features, train_targets, validation_features, validation_targets)
            return model_transformer.predict(validation_features)

        validation_predictions = model(train_data, validation_data)

        job = validation_predictions.run()

        job.wait_for_deployment_to_complete()

        production_dataset = pandas.DataFrame({
            "Sex": [0, 1],
            "Cabin": [101, 202],
            "Fare": [10, 60]
        })

        job_id = job.job_name()

        model_package = foundations.production.load_model_package(job_id)

        preprocessed_production_dataset = model_package.preprocessor(production_dataset)

        production_predictions = model_package.model.predict(preprocessed_production_dataset)

        @foundations.create_stage
        def log_predictions_for_assertion(predictions):
            foundations.log_metric("predictions", list(predictions["Survived"]))

        production_job = log_predictions_for_assertion(production_predictions).run()

        production_job.wait_for_deployment_to_complete()

        metrics = foundations.get_metrics_for_all_jobs('production_titanic_test')

        production_predictions = metrics.loc[metrics['job_id'] == production_job.job_name()].iloc[0]['predictions']

        self.assertEqual([1,0], production_predictions)
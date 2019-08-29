"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

from foundations_orbit_rest_api.v1.models.production_metric_set import ProductionMetricSet

class TestProductionMetricSet(Spec):

    @let_now
    def redis_connection(self):
        import fakeredis
        return self.patch('foundations_contrib.global_state.redis_connection', fakeredis.FakeRedis())

    @let_now
    def environ(self):
        fake_environ = {}
        fake_environ['MODEL_NAME'] = self.model_name
        fake_environ['PROJECT_NAME'] = self.project_name
        return self.patch('os.environ', fake_environ)

    @tear_down
    def tear_down(self):
        self.redis_connection.flushall()

    @let
    def model_name(self):
        return self.faker.uuid4()

    @let
    def project_name(self):
        return self.faker.word()

    @let
    def yAxisName(self):
        return self.faker.word()

    @let
    def yAxis(self):
        return {'title': {'text': self.yAxisName}}

    @let
    def title(self):
        return {'text': f'{self.yAxisName} over time'}

    @let
    def xAxis(self):
        category_set = []

        for _ in range(4):
            category_set.append(self.faker.word())

        return {'categories': category_set}

    @let
    def series(self):
        series = []

        for _ in range(2):
            data_set = []

            for _ in range(4):
                data_set.append(self.faker.random.random())

            series.append({'data': data_set, 'name': self.faker.word()})

        return series

    @let
    def metric_name(self):
        return self.faker.word()

    @let
    def metric_column(self):
        return self.faker.word()

    @let
    def metric_value(self):
        return self.faker.random.random()

    @let
    def metric_name_2(self):
        return self.faker.word()

    @let
    def metric_column_2(self):
        return self.faker.word()

    @let
    def metric_value_2(self):
        return self.faker.random.random()

    def test_has_title(self):
        model = ProductionMetricSet(title=self.title)
        self.assertEqual(self.title, model.title)

    def test_has_y_axis(self):
        model = ProductionMetricSet(yAxis=self.yAxis)
        self.assertEqual(self.yAxis, model.yAxis)
    
    def test_has_x_axis(self):
        model = ProductionMetricSet(xAxis=self.xAxis)
        self.assertEqual(self.xAxis, model.xAxis)
    
    def test_has_series(self):
        model = ProductionMetricSet(series=self.series)
        self.assertEqual(self.series, model.series)

    def test_all_returns_promise_with_empty_list_if_no_metrics_logged(self):
        promise = ProductionMetricSet.all(self.project_name)
        self.assertEqual([], promise.evaluate())

    def test_all_returns_promise_with_singleton_list_containing_one_empty_metric_set_if_metric_logged_with_no_values(self):
        from foundations_orbit import track_production_metrics

        self.environ['PROJECT_NAME'] = self.project_name
        self.environ['MODEL_NAME'] = self.model_name

        track_production_metrics(self.metric_name, {})

        promise = ProductionMetricSet.all(self.project_name)

        expected_metric_set = ProductionMetricSet(
            title={'text': f'{self.metric_name} over time'},
            yAxis={'title': {'text': self.metric_name}},
            xAxis={'categories': []},
            series={'data': [], 'name': self.model_name}
        )

        self.assertEqual([expected_metric_set], promise.evaluate())

    def test_all_returns_promise_with_singleton_list_containing_singleton_metric_set_if_metric_logged_with_one_key_value_pair(self):
        from foundations_orbit import track_production_metrics

        self.environ['PROJECT_NAME'] = self.project_name
        self.environ['MODEL_NAME'] = self.model_name

        track_production_metrics(self.metric_name, {self.metric_column: self.metric_value})

        promise = ProductionMetricSet.all(self.project_name)

        expected_metric_set = ProductionMetricSet(
            title={'text': f'{self.metric_name} over time'},
            yAxis={'title': {'text': self.metric_name}},
            xAxis={'categories': [self.metric_column]},
            series={'data': [self.metric_value], 'name': self.model_name}
        )

        self.assertEqual([expected_metric_set], promise.evaluate())
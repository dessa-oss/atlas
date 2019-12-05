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
        fake_environ['MONITOR_NAME'] = self.monitor_name
        fake_environ['PROJECT_NAME'] = self.project_name
        return self.patch('os.environ', fake_environ)

    @tear_down
    def tear_down(self):
        self.redis_connection.flushall()

    @let
    def monitor_name(self):
        return self.faker.uuid4()

    @let
    def monitor_name_2(self):
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
    def time_format_1(self):
        return 'January 21, 2019'

    @let
    def timestamp_format_1(self):
        return self._convert_formatted_date_string_to_timestamp(self.time_format_1)

    @let
    def time_format_2(self):
        return 'oct. 2/2007'

    @let
    def timestamp_format_2(self):
        return self._convert_formatted_date_string_to_timestamp(self.time_format_2)

    @let
    def time_format_3(self):
        return '10/13/1998 10:30PM'

    @let
    def timestamp_format_3(self):
        return self._convert_formatted_date_string_to_timestamp(self.time_format_3)

    @let
    def time_format_4(self):
        return '09/1972 23:30:43'

    @let
    def timestamp_format_4(self):
        return self._convert_formatted_date_string_to_timestamp(self.time_format_4)

    @let
    def date_time(self):
        return self.faker.date_time()

    @let
    def date_timestamp(self):
        return self._convert_datetime_object_to_timestamp(self.date_time)

    @let
    def metric_column(self):
        time = self.faker.date_time()
        return str(time)

    @let
    def metric_value(self):
        return self.faker.random.random()

    @let
    def metric_name_2(self):
        return self.faker.word()

    @let
    def metric_column_2(self):
        time = self.faker.date_time()
        return str(time)

    @let
    def metric_value_2(self):
        return self.faker.random.random()

    @let
    def metric_value_3(self):
        return self.faker.random.random()

    @let
    def metric_value_4(self):
        return self.faker.random.random()

    @let
    def timestamp(self):
        date_string = self.metric_column
        return self._convert_date_string_to_timestamp(date_string)

    @let
    def timestamp_2(self):
        date_string = self.metric_column_2
        return self._convert_date_string_to_timestamp(date_string)

    def _convert_datetime_object_to_timestamp(self, datetime):
        from dateutil import parser
        return datetime.timestamp() * 1000

    def _convert_formatted_date_string_to_timestamp(self, date_string):
        from dateutil import parser

        datetime = parser.parse(date_string)
        return datetime.timestamp() * 1000

    def _convert_date_string_to_timestamp(self, date_string):
        from datetime import datetime
        return datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S").timestamp() * 1000

    def test_has_title(self):
        monitor = ProductionMetricSet(title=self.title)
        self.assertEqual(self.title, monitor.title)

    def test_has_y_axis(self):
        monitor = ProductionMetricSet(yAxis=self.yAxis)
        self.assertEqual(self.yAxis, monitor.yAxis)
    
    def test_has_x_axis(self):
        monitor = ProductionMetricSet(xAxis=self.xAxis)
        self.assertEqual(self.xAxis, monitor.xAxis)
    
    def test_has_series(self):
        monitor = ProductionMetricSet(series=self.series)
        self.assertEqual(self.series, monitor.series)

    def test_all_returns_promise_with_empty_list_if_no_metrics_logged(self):
        promise = ProductionMetricSet.all(self.project_name)
        self.assertEqual([], promise.evaluate())

    def test_all_returns_promise_with_singleton_list_containing_one_empty_metric_set_if_metric_logged_with_no_values(self):
        from foundations_orbit import track_production_metrics

        self.environ['PROJECT_NAME'] = self.project_name
        self.environ['MONITOR_NAME'] = self.monitor_name

        track_production_metrics(self.metric_name, {})

        promise = ProductionMetricSet.all(self.project_name)

        expected_metric_set = ProductionMetricSet(
            title={'text': f'{self.metric_name} over time'},
            yAxis={'title': {'text': self.metric_name}},
            xAxis={'type': 'datetime'},
            series=[{'data': [], 'name': self.monitor_name}]
        )

        self.assertEqual([expected_metric_set], promise.evaluate())

    def test_all_returns_promise_with_singleton_list_containing_singleton_metric_set_if_metric_logged_with_one_key_value_pair(self):
        from foundations_orbit import track_production_metrics

        self.environ['PROJECT_NAME'] = self.project_name
        self.environ['MONITOR_NAME'] = self.monitor_name

        track_production_metrics(self.metric_name, {self.metric_column: self.metric_value})

        promise = ProductionMetricSet.all(self.project_name)

        expected_metric_set = ProductionMetricSet(
            title={'text': f'{self.metric_name} over time'},
            yAxis={'title': {'text': self.metric_name}},
            xAxis={'type': 'datetime'},
            series=[{'data': [[self.timestamp, self.metric_value]], 'name': self.monitor_name}]
        )

        self.assertEqual([expected_metric_set], promise.evaluate())

    def test_all_returns_promise_with_singleton_list_containing_singleton_metric_set_if_metric_logged_with_one_key_value_pair_using_datetime_object_as_date(self):
        from foundations_orbit import track_production_metrics

        self.environ['PROJECT_NAME'] = self.project_name
        self.environ['MONITOR_NAME'] = self.monitor_name

        track_production_metrics(self.metric_name, {self.date_time: self.metric_value})

        promise = ProductionMetricSet.all(self.project_name)

        expected_metric_set = ProductionMetricSet(
            title={'text': f'{self.metric_name} over time'},
            yAxis={'title': {'text': self.metric_name}},
            xAxis={'type': 'datetime'},
            series=[{'data': [[self.date_timestamp, self.metric_value]], 'name': self.monitor_name}]
        )

        self.assertEqual([expected_metric_set], promise.evaluate())

    def test_all_returns_promise_with_singleton_list_containing_metric_set_if_metric_logged_with_multiple_key_value_pairs(self):
        from foundations_orbit import track_production_metrics

        self.environ['PROJECT_NAME'] = self.project_name
        self.environ['MONITOR_NAME'] = self.monitor_name

        track_production_metrics(self.metric_name, {self.metric_column: self.metric_value, self.metric_column_2: self.metric_value_2})

        promise = ProductionMetricSet.all(self.project_name)

        expected_metric_set = ProductionMetricSet(
            title={'text': f'{self.metric_name} over time'},
            yAxis={'title': {'text': self.metric_name}},
            xAxis={'type': 'datetime'},
            series=[{'data': [[self.timestamp, self.metric_value], [self.timestamp_2, self.metric_value_2]], 'name': self.monitor_name}]
        )

        self.assertEqual([expected_metric_set], promise.evaluate())

    def test_all_returns_promise_with_singleton_list_containing_metric_set_if_metric_logged_with_multiple_key_value_pairs_with_varying_datetime_formats(self):
        from foundations_orbit import track_production_metrics

        self.environ['PROJECT_NAME'] = self.project_name
        self.environ['MONITOR_NAME'] = self.monitor_name

        track_production_metrics(self.metric_name, {
            self.time_format_1: self.metric_value,
            self.time_format_2: self.metric_value_2,
            self.time_format_3: self.metric_value_3,
            self.time_format_4: self.metric_value_4
        })

        promise = ProductionMetricSet.all(self.project_name)

        expected_metric_set = ProductionMetricSet(
            title={'text': f'{self.metric_name} over time'},
            yAxis={'title': {'text': self.metric_name}},
            xAxis={'type': 'datetime'},
            series=[{'data': [
                [self.timestamp_format_1, self.metric_value],
                [self.timestamp_format_2, self.metric_value_2],
                [self.timestamp_format_3, self.metric_value_3],
                [self.timestamp_format_4, self.metric_value_4]
            ], 'name': self.monitor_name}]
        )

        self.assertEqual([expected_metric_set], promise.evaluate())

    def test_all_returns_promise_with_list_containing_metric_sets_if_multiple_metric_names_logged(self):
        from foundations_orbit import track_production_metrics

        self.environ['PROJECT_NAME'] = self.project_name
        self.environ['MONITOR_NAME'] = self.monitor_name

        track_production_metrics(self.metric_name, {self.metric_column: self.metric_value})
        track_production_metrics(self.metric_name_2, {self.metric_column_2: self.metric_value_2})

        promise = ProductionMetricSet.all(self.project_name)

        expected_metric_set_0 = ProductionMetricSet(
            title={'text': f'{self.metric_name} over time'},
            yAxis={'title': {'text': self.metric_name}},
            xAxis={'type': 'datetime'},
            series=[{'data': [[self.timestamp, self.metric_value]], 'name': self.monitor_name}]
        )

        expected_metric_set_1 = ProductionMetricSet(
            title={'text': f'{self.metric_name_2} over time'},
            yAxis={'title': {'text': self.metric_name_2}},
            xAxis={'type': 'datetime'},
            series=[{'data': [[self.timestamp_2, self.metric_value_2]], 'name': self.monitor_name}]
        )

        self.assertEqual([expected_metric_set_0, expected_metric_set_1], promise.evaluate())


    def test_all_returns_promise_with_list_containing_metric_sets_if_multiple_metric_names_logged_multiple_with_monitor_names(self):
        from foundations_orbit import track_production_metrics

        self.environ['PROJECT_NAME'] = self.project_name

        self.environ['MONITOR_NAME'] = self.monitor_name

        track_production_metrics(self.metric_name, {self.metric_column: self.metric_value})
        track_production_metrics(self.metric_name_2, {self.metric_column_2: self.metric_value_2})

        self.environ['MONITOR_NAME'] = self.monitor_name_2

        track_production_metrics(self.metric_name, {self.metric_column: self.metric_value_3})
        track_production_metrics(self.metric_name_2, {self.metric_column_2: self.metric_value_4})

        promise = ProductionMetricSet.all(self.project_name)

        expected_metric_set_0 = ProductionMetricSet(
            title={'text': f'{self.metric_name} over time'},
            yAxis={'title': {'text': self.metric_name}},
            xAxis={'type': 'datetime'},
            series=[
                {'data': [[self.timestamp, self.metric_value]], 'name': self.monitor_name},
                {'data': [[self.timestamp, self.metric_value_3]], 'name': self.monitor_name_2}
            ]
        )

        expected_metric_set_1 = ProductionMetricSet(
            title={'text': f'{self.metric_name_2} over time'},
            yAxis={'title': {'text': self.metric_name_2}},
            xAxis={'type': 'datetime'},
            series=[
                {'data': [[self.timestamp_2, self.metric_value_2]], 'name': self.monitor_name},
                {'data': [[self.timestamp_2, self.metric_value_4]], 'name': self.monitor_name_2}
            ]
        )

        self.assertEqual([expected_metric_set_0, expected_metric_set_1], promise.evaluate())
"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

from foundations_orbit_rest_api.v1.models.production_metric_set import ProductionMetricSet

class TestProductionMetricSet(Spec):

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

    def test_has_title(self):
        model = ProductionMetricSet(title=self.title)
        self.assertEqual(self.title, model.title)

    
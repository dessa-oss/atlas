"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Dariem Perez <d.perez@dessa.com>, 11 2018
"""
import unittest
from foundations_rest_api.result_sorter import ResultSorter


class TestResultSorter(unittest.TestCase):

    class MockResultItem(object):

        def __init__(self, value1, value2=None):
            self.somefield = value1
            self.someotherfield = value2

    def setUp(self):
        self.item1 = self.MockResultItem('hello world 1', 3)
        self.item2 = self.MockResultItem('hello world 2', 3)
        self.item3 = self.MockResultItem('hello world 3', 1)

    def test_result_sorter_somefield_ascending(self):
        params = {'sort': 'somefield'}
        result_sorter = ResultSorter()
        initial_data = [self.item2, self.item3, self.item1]
        new_result = result_sorter(initial_data, params)
        self.assertEqual([self.item1, self.item2, self.item3], new_result)

    def test_result_sorter_key_not_presnt(self):
        params = {'random': 'somedata'}
        result_sorter = ResultSorter()
        initial_data = [self.item2, self.item3, self.item1]
        new_result = result_sorter(initial_data, params)
        self.assertEqual(initial_data, new_result)

    def test_result_sorter_somefield_descending(self):
        params = {'sort': '-somefield'}
        result_sorter = ResultSorter()
        initial_data = [self.item2, self.item3, self.item1]
        new_result = result_sorter(initial_data, params)
        self.assertEqual([self.item3, self.item2, self.item1], new_result)

    def test_result_sorter_someotherfield_ascending(self):
        params = {'sort': 'someotherfield'}
        result_sorter = ResultSorter()
        initial_data = [self.item2, self.item3, self.item1]
        new_result = result_sorter(initial_data, params)
        self.assertEqual([self.item3, self.item2, self.item1], new_result)

    def test_result_sorter_someotherfield_descending(self):
        params = {'sort': '-someotherfield'}
        result_sorter = ResultSorter()
        initial_data = [self.item2, self.item3, self.item1]
        new_result = result_sorter(initial_data, params)
        self.assertEqual([self.item2, self.item1, self.item3], new_result)

    def test_result_sorter_someotherfield_ascending_somefield_descending(self):
        params = {'sort': 'someotherfield,-somefield'}
        result_sorter = ResultSorter()
        initial_data = [self.item2, self.item3, self.item1]
        new_result = result_sorter(initial_data, params)
        self.assertEqual([self.item3, self.item2, self.item1], new_result)

    def test_result_sorter_someotherfield_ascending_somefield_ascending(self):
        params = {'sort': 'someotherfield,somefield'}
        result_sorter = ResultSorter()
        initial_data = [self.item2, self.item3, self.item1]
        new_result = result_sorter(initial_data, params)
        self.assertEqual([self.item3, self.item1, self.item2], new_result)

    def test_result_sorter_someotherfield_descending_somefield_ascending(self):
        params = {'sort': '-someotherfield,somefield'}
        result_sorter = ResultSorter()
        initial_data = [self.item2, self.item3, self.item1]
        new_result = result_sorter(initial_data, params)
        self.assertEqual([self.item1, self.item2, self.item3], new_result)

    def test_result_sorter_someotherfield_descending_somefield_descending(self):
        params = {'sort': '-someotherfield,-somefield'}
        result_sorter = ResultSorter()
        initial_data = [self.item2, self.item3, self.item1]
        new_result = result_sorter(initial_data, params)
        self.assertEqual([self.item2, self.item1, self.item3], new_result)

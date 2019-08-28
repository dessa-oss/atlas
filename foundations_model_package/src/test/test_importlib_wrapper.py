"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

from collections import namedtuple
from foundations_model_package.importlib_wrapper import load_function_from_module

class TestImportlibWrapper(Spec):

    mock_function = let_mock()
    mock_import = let_patch_mock_with_conditional_return('importlib.import_module')

    def test_load_function_from_module_returns_function_from_imported_module(self):
        mock_module = namedtuple('MockModule', ['this_function'])
        setattr(mock_module, 'this_function', self.mock_function)
        
        self.mock_import.return_when(mock_module, 'module_name')

        function = load_function_from_module('module_name', 'this_function')
        self.assertEqual(self.mock_function, function)

    def test_load_function_from_module_returns_function_from_imported_module(self):
        mock_module = namedtuple('MockModule', ['that_function'])
        setattr(mock_module, 'that_function', self.mock_function)
        
        self.mock_import.return_when(mock_module, 'module.name.inner')

        function = load_function_from_module('module.name.inner', 'that_function')
        self.assertEqual(self.mock_function, function)

    def test_load_function_from_module_raises_exception_if_module_not_found(self):
        mock_import = self.patch('importlib.import_module')
        mock_import.side_effect = ModuleNotFoundError()

        with self.assertRaises(Exception) as error_context:
            load_function_from_module('module_name', 'this_function')
        
        self.assertIn('Prediction module defined in manifest file could not be found!', error_context.exception.args)
        
    def test_load_function_from_module_raises_exception_from_original_exception_if_module_not_found(self):
        mock_import = self.patch('importlib.import_module')
        exception = ModuleNotFoundError()
        mock_import.side_effect = exception

        with self.assertRaises(Exception) as error_context:
            load_function_from_module('module_name', 'this_function')
        
        self.assertEqual(exception, error_context.exception.__cause__)

    def test_load_function_from_module_raises_exception_if_any_other_import_error(self):
        mock_import = self.patch('importlib.import_module')
        mock_import.side_effect = Exception()

        with self.assertRaises(Exception) as error_context:
            load_function_from_module('module_name', 'this_function')
        
        self.assertIn('Unable to load prediction module from manifest', error_context.exception.args)

    def test_load_function_from_module_raises_exception_from_original_exception_if_any_other_import_error(self):
        mock_import = self.patch('importlib.import_module')
        exception = Exception()
        mock_import.side_effect = exception

        with self.assertRaises(Exception) as error_context:
            load_function_from_module('module_name', 'this_function')
        
        self.assertEqual(exception, error_context.exception.__cause__)

    def test_load_function_from_module_raises_exception_if_function_not_in_module(self):
        mock_module = namedtuple('MockModule', [])
        
        self.mock_import.return_when(mock_module, 'module.name.inner')

        with self.assertRaises(Exception) as error_context:
            load_function_from_module('module.name.inner', 'that_function')
        
        self.assertIn('Prediction function defined in manifest file could not be found!', error_context.exception.args)
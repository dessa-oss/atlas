"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def load_function_from_module(module_name, function_name):
    import importlib

    module = _try_import(importlib.import_module, module_name)
    return _try_get_function(module, function_name)

def _try_import(importer, module_name):
    try:
        return importer(module_name)
    except ModuleNotFoundError as error:
        raise Exception('Prediction module defined in manifest file could not be found!') from error
    except Exception as error:
        raise Exception('Unable to load prediction module from manifest') from error

def _try_get_function(module, function_name):
    function = getattr(module, function_name, None)
    
    if function is None:
        raise Exception('Prediction function defined in manifest file could not be found!')

    return function
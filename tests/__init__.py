"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

import unittest

def suite_factory():
    loader = unittest.TestLoader()
    return loader.discover(".", pattern="test*.py")

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite_factory())
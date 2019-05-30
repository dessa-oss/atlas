"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def wait_five_seconds():
    import time
    time.sleep(5)

def finishes_instantly():
    pass

def function_that_prints():
    print("I am a function. I print things")

def fails_fast():
    raise RuntimeError('whoops')
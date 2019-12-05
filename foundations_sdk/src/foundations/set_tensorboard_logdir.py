"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

def set_tensorboard_logdir(path):
    import atexit
    import foundations

    atexit.register(_create_tensorboard_logdir(path))
    foundations.set_tag('tf', 'tf')

def _create_tensorboard_logdir(path):
    from foundations import create_syncable_directory
    
    tensorboard_logdir = create_syncable_directory('__tensorboard__', path)
    return lambda: tensorboard_logdir.upload()

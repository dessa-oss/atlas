
def set_tensorboard_logdir(path):
    import atexit
    import foundations

    atexit.register(_create_tensorboard_logdir(path))
    foundations.set_tag('tf', 'tf')

def _create_tensorboard_logdir(path):
    from foundations import create_syncable_directory
    
    tensorboard_logdir = create_syncable_directory('__tensorboard__', path)
    return lambda: tensorboard_logdir.upload()

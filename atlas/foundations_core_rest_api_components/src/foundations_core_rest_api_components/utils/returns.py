

def returns(*types):
    """Decorator for defining returns for controllers
    """
    def _internal(function):
        return function
    return _internal
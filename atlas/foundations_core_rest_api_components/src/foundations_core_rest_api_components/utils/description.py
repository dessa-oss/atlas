

def description(description):
    """Decorator for defining description for controllers
    """
    def _internal(klass):
        return klass
    return _internal
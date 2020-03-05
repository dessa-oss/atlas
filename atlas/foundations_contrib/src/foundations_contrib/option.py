

def Option(value):
    from foundations_contrib.something import Something
    from foundations_contrib.nothing import Nothing

    if isinstance(value, Nothing) or isinstance(value, Something):
        return value

    return Nothing() if value is None else Something(value)

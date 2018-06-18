def Option(value):
    from vcat.something import Something
    from vcat.nothing import Nothing

    if isinstance(value, Nothing) or isinstance(value, Something):
        return value

    return Nothing() if value is None else Something(value)

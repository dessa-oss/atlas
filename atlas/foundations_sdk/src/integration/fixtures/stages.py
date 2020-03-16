

def make_data(data='created some data here'):
    return data

def concat_data(left, right):
    return left + right

def divide_by_zero():
    return 1 / 0

def _make_generator():
    yield "beep"

_GENERATOR = _make_generator()

def returns_generator():
    return _GENERATOR

def returns_fresh_generator():
    return _make_generator()

def executes_generator(gen):
    return next(gen)
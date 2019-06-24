import foundations

_cached_function_was_run = False

def add(x,y):
    result = x + y
    foundations.log_metric('Score', result)

@foundations.cache
def subtract(x,y):
    global _cached_function_was_run

    if _cached_function_was_run:
        raise AssertionError('Function body should not be executed if function value already cached')
    
    result = x - y
    _cached_function_was_run = True
    return result



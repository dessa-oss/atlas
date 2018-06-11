from vcat.context_aware import ContextAware
import inspect

def getsource(func):
    if isinstance(func, ContextAware):
        return inspect.getsource(func._function)
    else:
        return inspect.getsource(func)

def getsourcefile(func):
    if isinstance(func, ContextAware):
        return inspect.getsourcefile(func._function)
    else:
        return inspect.getsourcefile(func)

def getsourcelines(func):
    if isinstance(func, ContextAware):
        return inspect.getsourcelines(func._function)
    else:
        return inspect.getsourcelines(func)

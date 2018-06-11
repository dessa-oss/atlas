class Lazy(object):
    def __init__(self, function, *args, **kwargs):
        def generate_thunk():
            yield function(*args, **kwargs)

        self._has_run = False
        self._internal = generate_thunk()

    def _eval(self):
        if not self._has_run:
            self._has_run = True
            self._internal = next(self._internal)

        return self._internal

def lazily(function):
    def lazy_function(*args, **kwargs):
        return Lazy(function, *args, **kwargs)

    return lazy_function

def _traverse_body(traversal, fold_action, this_node):
    return [traversal(fold_action, node) for node in this_node.previous_nodes()]

def traverse(fold_action, this_node):
    return fold_action(_traverse_body(traverse, fold_action, this_node), this_node)

def lazy_traverse(fold_action, this_node):
    _lazy_traverse_body = lazily(_traverse_body)
    return fold_action(_lazy_traverse_body(lazy_traverse, fold_action, this_node), this_node)

def force_results(lazy_value):
    return lazy_value._eval()
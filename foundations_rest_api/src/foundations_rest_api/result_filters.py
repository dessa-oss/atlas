

def sort_results(result, params):
    if 'sort' in params and isinstance(result, list):
        # TODO: do sorting
        pass
    return result

result_filters = [sort_results]